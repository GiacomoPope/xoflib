use pyo3::{exceptions::PyValueError, prelude::*, types::PyBytes};
use sha3::{
    digest::{
        core_api::{CoreWrapper, XofReaderCoreWrapper},
        ExtendableOutputReset, Update, XofReader,
    },
    Shake128, Shake128ReaderCore, Shake256, Shake256ReaderCore, TurboShake128, TurboShake128Core,
    TurboShake128ReaderCore, TurboShake256, TurboShake256Core, TurboShake256ReaderCore,
};

macro_rules! impl_sponge_shaker_classes {
    // hasher is tt so we can pick the right kind of methods to generate
    (hasher_name = $hasher:tt, pyclass_name = $class_name:literal, reader_name = $xof_reader:ident, rust_shaker_name = $shaker_name:ident, rust_sponge_name = $sponge_name:ident) => {
        #[pyclass(module="xoflib", name=$class_name)]
        #[doc=concat!(stringify!($shaker_name), " implements absorption and finalization for the ", stringify!($hasher), " XOF")]
        struct $shaker_name {
            hasher: $hasher,
        }

        impl_sponge_shaker_classes!(@shaker_methods $hasher, $shaker_name, $sponge_name);

        #[pyclass(module="xoflib")]
        #[doc=concat!(stringify!($sponge_name), " implements sponge expansion for the ", stringify!($hasher), " XOF")]
        struct $sponge_name {
            xof: XofReaderCoreWrapper<$xof_reader>,
        }

        #[pymethods]
        impl $sponge_name {
            #[doc=concat!("Read `n` bytes of data from the ", stringify!($hasher), " XOF")]
            fn read<'py>(&mut self, py: Python<'py>, n: usize) -> PyResult<Bound<'py, PyBytes>> {
                PyBytes::new_bound_with(py, n, |bytes| {
                    self.xof.read(bytes);
                    Ok(())
                })
            }

            fn __repr__(&self) -> String {
                String::from(stringify!($sponge_name))
            }

            fn __str__(&self) -> String {
                self.__repr__()
            }
        }
    };

    // "match" on the TurboShakes and generate a unique __init__ for them with domain separation
    (@shaker_methods TurboShake128, $shaker_name:ident, $sponge_name:ident) => {
        impl_sponge_shaker_classes!(@turbo_shaker_methods TurboShake128Core, $shaker_name, $sponge_name);
    };

    (@shaker_methods TurboShake256, $shaker_name:ident, $sponge_name:ident) => {
        impl_sponge_shaker_classes!(@turbo_shaker_methods TurboShake256Core, $shaker_name, $sponge_name);
    };

    (@turbo_shaker_methods $hasher_core:ident, $shaker_name:ident, $sponge_name:ident) => {
        #[pymethods]
        impl $shaker_name {
            #[new]
            #[pyo3(signature = (domain_sep, input_bytes = None))]
            fn new(domain_sep: u8, input_bytes: Option<&[u8]>) -> PyResult<Self> {
                if !(0x01..=0x7F).contains(&domain_sep) {
                    return Err(PyValueError::new_err("domain sep is not in range(1, 0x80)"))
                }

                let mut hasher = CoreWrapper::from_core($hasher_core::new(domain_sep));
                if let Some(initial_data) = input_bytes {
                    hasher.update(initial_data);
                }

                Ok(Self { hasher })
            }

            #[doc=concat!("Absorb `input_bytes` into the ", stringify!($hasher_core), " state")]
            fn absorb(&mut self, input_bytes: &[u8]) {
                self.hasher.update(input_bytes);
            }

            #[doc=concat!(
                "Finalize the ", stringify!($hasher_core), " XOF into a sponge for expansion\n",
                "\n",
                "This method also resets the state, allowing more data to be absorbed.",
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
    (@shaker_methods $hasher:ident, $shaker_name:ident, $sponge_name:ident) => {
        #[pymethods]
        impl $shaker_name {
            #[new]
            #[pyo3(signature = (input_bytes = None))]
            fn new(input_bytes: Option<&[u8]>) -> Self {
                let mut hasher = $hasher::default();
                if let Some(initial_data) = input_bytes {
                    hasher.update(initial_data);
                }
                Self { hasher }
            }

            #[doc=concat!("Absorb `input_bytes` into the ", stringify!($hasher), " state")]
            fn absorb(&mut self, input_bytes: &[u8]) {
                self.hasher.update(input_bytes);
            }

            #[doc=concat!(
                "Finalize the ", stringify!($hasher), " XOF into a sponge for expansion\n",
                "\n",
                "This method also resets the state, allowing more data to be absorbed.",
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

#[pyfunction]
fn shake128(data: &[u8]) -> Sponge128 {
    Shaker128::new(Some(data)).finalize()
}

#[pyfunction]
fn shake256(data: &[u8]) -> Sponge256 {
    Shaker256::new(Some(data)).finalize()
}

#[pyfunction]
fn turbo_shake128(domain_sep: u8, data: &[u8]) -> PyResult<TurboSponge128> {
    Ok(TurboShaker128::new(domain_sep, Some(data))?.finalize())
}

#[pyfunction]
fn turbo_shake256(domain_sep: u8, data: &[u8]) -> PyResult<TurboSponge256> {
    Ok(TurboShaker256::new(domain_sep, Some(data))?.finalize())
}

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

    Ok(())
}
