use pyo3::{exceptions::PyValueError, prelude::*, types::PyBytes};
use sha3::{
    digest::*, Shake128, Shake256, TurboShake128, TurboShake128Core, TurboShake256,
    TurboShake256Core,
};

macro_rules! impl_shaker_and_sponge {
    ($shaker_name:ident, $sponge_name:ident, $inner:ty, default) => {
        impl_shaker_and_sponge!(@impl $shaker_name, $sponge_name, $inner, (), (), (Ok::<_, PyErr>(Default::default())));
    };

    ($shaker_name:ident, $sponge_name:ident, $inner:ty, $($argname:ident: $argty:ty),* => $create:ident $(| $($extra:tt)*)?) => {
        impl_shaker_and_sponge!(@impl $shaker_name,
                                      $sponge_name,
                                      $inner,
                                      ($($argname),*, ),
                                      ($($argname: $argty),*, ),
                                      ($create!($inner, $($argname),* $(| $($extra)*)?)));
    };

    (@impl $shaker_name:ident,
           $sponge_name:ident,
           $inner:ty,
           ($($new_sig:tt)*),
           ($($shaker_ctor_args:tt)*),
           ($($shaker_ctor:tt)*)) => {
        #[pyclass]
        struct $shaker_name(Shaker<$inner>);

        #[pymethods]
        impl $shaker_name {
            #[new]
            #[pyo3(signature = ($($new_sig)* input_bytes = None))]
            fn new($($shaker_ctor_args)* input_bytes: Option<&[u8]>) -> PyResult<Self> {
                let mut res = Self($($shaker_ctor)*?);
                if let Some(input) = input_bytes {
                    res.absorb(input)?;
                }
                Ok(res)
            }

            fn absorb(&mut self, input_bytes: &[u8]) -> PyResult<()> {
                self.0.absorb(input_bytes)
            }

            fn finalize(&mut self) -> PyResult<$sponge_name> {
                Ok($sponge_name(self.0.finalize()?))
            }
        }

        #[pyclass]
        struct $sponge_name(Sponge<$inner>);

        #[pymethods]
        impl $sponge_name {
            fn read<'py>(&mut self, py: Python<'py>, n: usize) -> PyResult<Bound<'py, PyBytes>> {
                PyBytes::new_bound_with(py, n, |buffer| self.0.read_into(buffer))
            }

            // Can't really do this cleanly without unsafe :/
            // fn read_into<'py>(
            //     &mut self,
            //     py: Python<'py>,
            //     buffer: Bound<'py, PyByteArray>,
            // ) -> PyResult<()> {
            //     self.0.read_into(buffer)
            // }

            fn __repr__(&self) -> String {
                String::from(stringify!($sponge_name))
            }

            fn __str__(&self) -> String {
                self.__repr__()
            }
        }
    };
}

#[derive(Default)]
struct Shaker<H>(H);

impl<H> Shaker<H>
where
    H: ExtendableOutputReset,
{
    fn absorb(&mut self, data: &[u8]) -> PyResult<()> {
        Ok(self.0.update(data))
    }

    fn finalize(&mut self) -> PyResult<Sponge<H>> {
        Ok(Sponge(self.0.finalize_xof_reset()))
    }
}

struct Sponge<H: ExtendableOutputReset>(H::Reader);

impl<H: ExtendableOutputReset> Sponge<H> {
    fn read_into(&mut self, out: &mut [u8]) -> PyResult<()> {
        Ok(self.0.read(out))
    }
}

macro_rules! turboshake_create {
    ($name:ty, $domain_sep:ident | $core:ident) => {
        if (0x01..=0x7F).contains(&$domain_sep) {
            Ok(Shaker(<$name>::from_core($core::new($domain_sep))))
        } else {
            Err(PyValueError::new_err(
                "Domain separator not in range(1, 0x80)",
            ))
        }
    };
}

impl_shaker_and_sponge!(Shaker128, Sponge128, Shake128, default);
impl_shaker_and_sponge!(Shaker256, Sponge256, Shake256, default);
impl_shaker_and_sponge!(
    TurboShaker128,
    TurboSponge128,
    TurboShake128,
    domain_sep: u8 => turboshake_create | TurboShake128Core
);
impl_shaker_and_sponge!(
    TurboShaker256,
    TurboSponge256,
    TurboShake256,
    domain_sep: u8 => turboshake_create | TurboShake256Core
);

/// A Python module implemented in Rust.
#[pymodule]
fn xof_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Sponge128>()?;
    m.add_class::<Shaker128>()?;
    m.add_class::<Sponge256>()?;
    m.add_class::<Shaker256>()?;
    m.add_class::<TurboSponge128>()?;
    m.add_class::<TurboShaker128>()?;
    m.add_class::<TurboSponge256>()?;
    m.add_class::<TurboShaker256>()?;

    Ok(())
}
