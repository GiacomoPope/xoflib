use ascon_hash::{AsconAXof, AsconAXofReaderCore, AsconXof, AsconXofReaderCore};
use pyo3::{
    buffer::PyBuffer,
    exceptions::{PyTypeError, PyValueError},
    prelude::*,
    types::PyBytes,
};
use sha3::{
    digest::{
        core_api::{CoreWrapper, XofReaderCoreWrapper},
        ExtendableOutputReset, Update, XofReader,
    },
    Shake128, Shake128ReaderCore, Shake256, Shake256ReaderCore, TurboShake128, TurboShake128Core,
    TurboShake128ReaderCore, TurboShake256, TurboShake256Core, TurboShake256ReaderCore,
};

fn pybuffer_get_bytes<'py>(data: &Bound<'py, PyAny>) -> PyResult<&'py [u8]> {
    let buf = PyBuffer::<u8>::get_bound(data)?;

    // SAFETY: we hold the GIL so it is safe to access data via buffer.buf_ptr
    Ok(unsafe { std::slice::from_raw_parts(buf.buf_ptr() as *const _, buf.len_bytes()) })
}

fn pybuffer_get_bytes_mut<'py>(data: &Bound<'py, PyAny>) -> PyResult<&'py mut [u8]> {
    let buf = PyBuffer::<u8>::get_bound(data)?;

    // SAFETY PRECONDITION: Ensure the data area is mutable
    if buf.readonly() {
        return Err(PyTypeError::new_err("Cannot write into readonly object"));
    }

    // SAFETY: we hold the GIL so it is safe to access data via buffer.buf_ptr
    Ok(unsafe { std::slice::from_raw_parts_mut(buf.buf_ptr() as *mut _, buf.len_bytes()) })
}

macro_rules! impl_sponge_shaker_classes {
    // hasher is tt so we can pick the right kind of methods to generate
    (hasher_name = $hasher:tt, pyclass_name = $class_name:literal, reader_name = $xof_reader:ident, rust_shaker_name = $shaker_name:ident, rust_sponge_name = $sponge_name:ident $(,)?) => {
        #[pyclass(module="xoflib", name=$class_name)]
        #[doc=concat!(stringify!($shaker_name), " implements absorption and finalization for the ", stringify!($hasher), " XOF")]
        struct $shaker_name {
            hasher: $hasher,
        }

        impl_sponge_shaker_classes!(@shaker_methods $hasher, $class_name, $shaker_name, $sponge_name);

        #[pyclass(module="xoflib")]
        #[doc=concat!(stringify!($sponge_name), " implements sponge expansion for the ", stringify!($hasher), " XOF")]
        struct $sponge_name {
            xof: XofReaderCoreWrapper<$xof_reader>,
        }

        #[pymethods]
        impl $sponge_name {
            #[doc=concat!(
                "Read `n` bytes of data from the ", stringify!($hasher), " XOF\n",
                "\n",
                "Example:\n",
                "\n",
                ".. code-block:: python\n",
                "\n",
                "   >>> from xoflib import ", $class_name, "\n",
                "   >>> xof = ", impl_sponge_shaker_classes!(@docs_construct_hasher $hasher, $class_name), "\n",
                "   >>> xof = xof.absorb(bytearray(b\"Ooh just a little bit more data\")).finalize()\n",
                "   >>> xof.read(16).hex()\n",
                "   ", impl_sponge_shaker_classes!(@docs_example_hash $hasher), "\n",
            )]
            fn read<'py>(&mut self, py: Python<'py>, n: usize) -> PyResult<Bound<'py, PyBytes>> {
                PyBytes::new_bound_with(py, n, |bytes| {
                    self.xof.read(bytes);
                    Ok(())
                })
            }

            #[doc=concat!(
                "Fill the input buffer with data from the ", stringify!($hasher), " XOF",
                "\n",
                "Example:\n",
                "\n",
                ".. code-block:: python\n",
                "\n",
                "   >>> from xoflib import ", $class_name, "\n",
                "   >>> xof = ", impl_sponge_shaker_classes!(@docs_construct_hasher $hasher, $class_name), "\n",
                "   >>> xof = xof.absorb(bytearray(b\"Ooh just a little bit more data\")).finalize()\n",
                "   >>> buf = bytearray(b\"\\0\" * 10)\n",
                "   >>> xof.read_into(buf)\n",
                "   >>> buf.hex()\n",
                "   ", impl_sponge_shaker_classes!(@docs_example_hash $hasher), "\n",
            )]
            fn read_into(&mut self, buf: &Bound<'_, PyAny>) -> PyResult<()> {
                self.xof.read(pybuffer_get_bytes_mut(buf)?);
                Ok(())
            }

            fn __repr__(&self) -> String {
                String::from(stringify!($sponge_name))
            }

            fn __str__(&self) -> String {
                self.__repr__()
            }
        }
    };

    // "match" on the TurboShakes and generate the correct constructor for them
    (@docs_construct_hasher TurboShake128, $class_name:literal) => {
        concat!($class_name, "(1, b\"bytes to absorb\")")
    };

    (@docs_construct_hasher TurboShake256, $class_name:literal) => {
        concat!($class_name, "(1, b\"bytes to absorb\")")
    };

    (@docs_construct_hasher $hasher:ident, $class_name:literal) => {
        concat!($class_name, "(b\"bytes to absorb\")")
    };

    // "match" on the hasher and generate the correct hash for the example
    (@docs_example_hash Shake128) => {
        "'2c67a3c30e75de37d30e3f6d94e05a00'"
    };

    (@docs_example_hash Shake256) => {
        "'82786e027034dccb6f41224c22a227c9'"
    };

    (@docs_example_hash TurboShake128) => {
        "'b6be317e80aa741b9f0ac9330d584506'"
    };

    (@docs_example_hash TurboShake256) => {
        "'2e9d18d326438ea968b071ab958f6260'"
    };

    (@docs_example_hash AsconXof) => {
        "'202e12280fb6781470016dc067d3b213'"
    };

    (@docs_example_hash AsconAXof) => {
        "'e3d5593d0e08c5a7c6cbf751fb817f0a'"
    };

    // "match" on the TurboShakes and generate a unique __init__ for them with domain separation
    (@shaker_methods TurboShake128, $class_name:literal, $shaker_name:ident, $sponge_name:ident) => {
        impl_sponge_shaker_classes!(@turbo_shaker_methods TurboShake128Core, $class_name, $shaker_name, $sponge_name);
    };

    (@shaker_methods TurboShake256, $class_name:literal, $shaker_name:ident, $sponge_name:ident) => {
        impl_sponge_shaker_classes!(@turbo_shaker_methods TurboShake256Core, $class_name, $shaker_name, $sponge_name);
    };

    (@turbo_shaker_methods $hasher_core:ident, $class_name:literal, $shaker_name:ident, $sponge_name:ident) => {
        #[pymethods]
        impl $shaker_name {
            #[new]
            #[pyo3(signature = (domain_sep, input_bytes = None))]
            fn new(domain_sep: u8, input_bytes: Option<&Bound<'_, PyAny>>) -> PyResult<Self> {
                if !(0x01..=0x7F).contains(&domain_sep) {
                    return Err(PyValueError::new_err("domain sep is not in range(1, 0x80)"))
                }

                let mut hasher = CoreWrapper::from_core($hasher_core::new(domain_sep));
                if let Some(initial_data) = input_bytes {
                    hasher.update(pybuffer_get_bytes(initial_data)?);
                }

                Ok(Self { hasher })
            }

            #[doc=concat!(
                "Absorb `input_bytes` into the ", stringify!($hasher_core), " state\n",
                "\n",
                "Note: this method can be chained, i.e. .absorb().absorb()\n",
                "\n",
                "Example:\n",
                "\n",
                ".. code-block:: python\n",
                "\n",
                "   >>> from xoflib import ", $class_name, "\n",
                "   >>> xof = ", $class_name, "(1, b\"Some initial data\")\n",
                "   >>> xof.absorb(bytearray(b\"Ooh just a little bit more data\"))\n",
            )]
            fn absorb<'py>(mut slf: PyRefMut<'py, Self>, input_bytes: &Bound<'py, PyAny>) -> PyResult<PyRefMut<'py, Self>> {
                slf.hasher.update(pybuffer_get_bytes(input_bytes)?);
                Ok(slf)
            }

            #[doc=concat!(
                "Finalize the ", stringify!($hasher_core), " XOF into a sponge for expansion\n",
                "\n",
                "This method also resets the state, allowing more data to be absorbed.",
                "\n",
                "Example:\n",
                "\n",
                ".. code-block:: python\n",
                "\n",
                "   >>> from xoflib import ", $class_name, "\n",
                "   >>> xof = ", $class_name, "(1, b\"Some initial data\")\n",
                "   >>> xof = xof.finalize()\n",
            )]
            fn finalize(&mut self) -> $sponge_name {
                $sponge_name {
                    xof: self.hasher.finalize_xof_reset(),
                }
            }

            fn __repr__(&self) -> String {
                String::from(stringify!($shaker_name))
            }

            fn __str__(&self) -> String {
                self.__repr__()
            }
        }
    };

    // I would love to be more specific with the template but annoyingly you cannot use a macro in
    // a #[pymethods] block to define methods :(
    (@shaker_methods $hasher:ident, $class_name:literal, $shaker_name:ident, $sponge_name:ident) => {
        #[pymethods]
        impl $shaker_name {
            #[new]
            #[pyo3(signature = (input_bytes = None))]
            fn new(input_bytes: Option<&Bound<'_, PyAny>>) -> PyResult<Self> {
                let mut hasher = $hasher::default();
                if let Some(initial_data) = input_bytes {
                    hasher.update(pybuffer_get_bytes(initial_data)?);
                }
                Ok(Self { hasher })
            }

            #[doc=concat!(
                "Absorb `input_bytes` into the ", stringify!($hasher), " state\n",
                "\n",
                "Note: this method can be chained, i.e. .absorb().absorb()\n",
                "\n",
                "Example:\n",
                "\n",
                ".. code-block:: python\n",
                "\n",
                "   >>> from xoflib import ", $class_name, "\n",
                "   >>> xof = ", $class_name, "(b\"Some initial data\")\n",
                "   >>> xof.absorb(bytearray(b\"Ooh just a little bit more data\"))\n",
            )]
            fn absorb<'py>(mut slf: PyRefMut<'py, Self>, input_bytes: &Bound<'py, PyAny>) -> PyResult<PyRefMut<'py, Self>> {
                slf.hasher.update(pybuffer_get_bytes(input_bytes)?);
                Ok(slf)
            }

            #[doc=concat!(
                "Finalize the ", stringify!($hasher), " XOF into a sponge for expansion\n",
                "\n",
                "This method also resets the state, allowing more data to be absorbed.",
                "\n",
                "Example:\n",
                "\n",
                ".. code-block:: python\n",
                "\n",
                "   >>> from xoflib import ", $class_name, "\n",
                "   >>> xof = ", $class_name, "(b\"Some initial data\")\n",
                "   >>> xof = xof.finalize()\n",
            )]
            fn finalize(&mut self) -> $sponge_name {
                $sponge_name {
                    xof: self.hasher.finalize_xof_reset(),
                }
            }

            fn __repr__(&self) -> String {
                String::from(stringify!($shaker_name))
            }

            fn __str__(&self) -> String {
                self.__repr__()
            }
        }
    };
}

#[rustfmt::skip]
impl_sponge_shaker_classes!(
    hasher_name      = Shake128,
    pyclass_name     = "Shake128",
    reader_name      = Shake128ReaderCore,
    rust_shaker_name = Shaker128,
    rust_sponge_name = Sponge128
);
#[rustfmt::skip]
impl_sponge_shaker_classes!(
    hasher_name      = Shake256,
    pyclass_name     = "Shake256",
    reader_name      = Shake256ReaderCore,
    rust_shaker_name = Shaker256,
    rust_sponge_name = Sponge256
);
#[rustfmt::skip]
impl_sponge_shaker_classes!(
    hasher_name      = TurboShake128,
    pyclass_name     = "TurboShake128",
    reader_name      = TurboShake128ReaderCore,
    rust_shaker_name = TurboShaker128,
    rust_sponge_name = TurboSponge128
);
#[rustfmt::skip]
impl_sponge_shaker_classes!(
    hasher_name      = TurboShake256,
    pyclass_name     = "TurboShake256",
    reader_name      = TurboShake256ReaderCore,
    rust_shaker_name = TurboShaker256,
    rust_sponge_name = TurboSponge256
);

#[rustfmt::skip]
impl_sponge_shaker_classes!(
    hasher_name      = AsconXof,
    pyclass_name     = "AsconXof",
    reader_name      = AsconXofReaderCore,
    rust_shaker_name = Ascon,
    rust_sponge_name = AsconSponge,
);
#[rustfmt::skip]
impl_sponge_shaker_classes!(
    hasher_name      = AsconAXof,
    pyclass_name     = "AsconAXof",
    reader_name      = AsconAXofReaderCore,
    rust_shaker_name = AsconA,
    rust_sponge_name = AsconASponge,
);

/// Construct a TurboSponge128 directly from `domain_sep` and `data`
///
/// Example:
///
/// .. code-block:: python
///
///    >>> from xoflib import turbo_shake128
///    >>> xof = turbo_shake128(1, b"bytes to absorb")
///    >>> xof.read(16).hex()
///    '4bb4e35b21335fcc6ae6cd3d0a5fe005'
#[pyfunction]
fn turbo_shake128(domain_sep: u8, data: &Bound<'_, PyAny>) -> PyResult<TurboSponge128> {
    Ok(TurboShaker128::new(domain_sep, Some(data))?.finalize())
}

/// Construct a TurboSponge256 directly from `domain_sep` and `data`
///
/// Example:
///
/// .. code-block:: python
///
///    >>> from xoflib import turbo_shake256
///    >>> xof = turbo_shake256(1, b"bytes to absorb")
///    >>> xof.read(16).hex()
///    'd671d0021e9f22293d062259e68e6e89'
#[pyfunction]
fn turbo_shake256(domain_sep: u8, data: &Bound<'_, PyAny>) -> PyResult<TurboSponge256> {
    Ok(TurboShaker256::new(domain_sep, Some(data))?.finalize())
}

#[rustfmt::skip]
macro_rules! impl_sponge_constructor {
    (function_name = $func_name:ident, xof = $xof:ident, sponge = $sponge:ident, example_hash = $example_hash:literal $(,)?) => {
        #[doc=concat!(
            "Construct a ", stringify!($sponge), " directly from `data`\n",
            "\n",
            "Example:\n",
            "\n",
            ".. code-block:: python\n",
            "\n",
            "   >>> from xoflib import ", stringify!($func_name), "\n",
            "   >>> xof = ", stringify!($func_name), "(b\"bytes to absorb\")\n",
            "   >>> xof.read(16).hex()\n",
            "   '", $example_hash, "'\n",
        )]
        #[pyfunction]
        fn $func_name(data: &Bound<'_, PyAny>) -> PyResult<$sponge> {
            Ok($xof::new(Some(data))?.finalize())
        }
    };
}

#[rustfmt::skip]
impl_sponge_constructor!(
    function_name = shake128,
    xof           = Shaker128,
    sponge        = Sponge128,
    example_hash  = "250ef380a0f0c92e9506af9893f640fa",
);
#[rustfmt::skip]
impl_sponge_constructor!(
    function_name = shake256,
    xof           = Shaker256,
    sponge        = Sponge256,
    example_hash  = "1e54f9f0cbacb3573a05dd5d48ea4104"
);

#[rustfmt::skip]
impl_sponge_constructor!(
    function_name = ascon_xof,
    xof           = Ascon,
    sponge        = AsconSponge,
    example_hash  = "d7bbe757e53015382e3ee13a2207fafc",
);
#[rustfmt::skip]
impl_sponge_constructor!(
    function_name = ascona_xof,
    xof           = AsconA,
    sponge        = AsconASponge,
    example_hash  = "ae7ba96550a57300da1e2ba31335d922",
);

/// A Python package for the Shake extendable-output functions (XOFs): Shake128,
/// Shake256 and the turbo variants built with pyO3 bindings to the sha3 Rust
/// crate.
#[pymodule]
fn xoflib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Sponge128>()?;
    m.add_class::<Shaker128>()?;
    m.add_class::<Sponge256>()?;
    m.add_class::<Shaker256>()?;
    m.add_class::<TurboSponge128>()?;
    m.add_class::<TurboShaker128>()?;
    m.add_class::<TurboSponge256>()?;
    m.add_class::<TurboShaker256>()?;

    m.add_function(wrap_pyfunction!(shake128, m)?)?;
    m.add_function(wrap_pyfunction!(shake256, m)?)?;
    m.add_function(wrap_pyfunction!(turbo_shake128, m)?)?;
    m.add_function(wrap_pyfunction!(turbo_shake256, m)?)?;

    m.add_class::<Ascon>()?;
    m.add_class::<AsconSponge>()?;
    m.add_class::<AsconA>()?;
    m.add_class::<AsconASponge>()?;

    m.add_function(wrap_pyfunction!(ascon_xof, m)?)?;
    m.add_function(wrap_pyfunction!(ascona_xof, m)?)?;

    Ok(())
}
