use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sha3::{
    digest::{
        core_api::XofReaderCoreWrapper, crypto_common::BlockSizeUser, ExtendableOutput, Update,
        XofReader,
    },
    Shake128, Shake128ReaderCore,
};

// Very silly first attempt at a class

#[pyclass(name = "Shake128_pyo3")]
struct Shake128Py {
    xof: XofReaderCoreWrapper<Shake128ReaderCore>,
}

#[pymethods]
impl Shake128Py {
    #[new]
    fn init(input_bytes: &[u8]) -> Self {
        let mut hasher = Shake128::default();
        hasher.update(input_bytes);
        let xof: XofReaderCoreWrapper<sha3::Shake128ReaderCore> = hasher.finalize_xof();
        Self { xof }
    }

    fn read<'py>(&mut self, py: Python<'py>, n: usize) -> PyResult<Bound<'py, PyBytes>> {
        PyBytes::new_bound_with(py, n, |bytes| Ok(self.xof.read(bytes)))
    }
}

// Some simple functions used for testing

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128<'py>(
    py: Python<'py>,
    input_bytes: &[u8],
    n: usize,
) -> PyResult<pyo3::Bound<'py, PyBytes>> {
    let mut hasher = Shake128::default();
    hasher.update(input_bytes);
    let mut xof: sha3::digest::core_api::XofReaderCoreWrapper<sha3::Shake128ReaderCore> =
        hasher.finalize_xof();
    PyBytes::new_bound_with(py, n, |bytes: &mut [u8]| Ok(xof.read(bytes)))
}

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128_one_block<'py>(
    py: Python<'py>,
    input_bytes: &[u8],
) -> PyResult<Bound<'py, PyBytes>> {
    pyo3_shake_128_n_blocks(py, input_bytes, 1)
}

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128_n_blocks<'py>(
    py: Python<'py>,
    input_bytes: &[u8],
    n: usize,
) -> PyResult<Bound<'py, PyBytes>> {
    pyo3_shake_128(py, input_bytes, n * Shake128::block_size())
}

/// A Python module implemented in Rust.
#[pymodule]
fn xof_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pyo3_shake_128, m)?)?;
    m.add_function(wrap_pyfunction!(pyo3_shake_128_one_block, m)?)?;
    m.add_function(wrap_pyfunction!(pyo3_shake_128_n_blocks, m)?)?;
    m.add_class::<Shake128Py>()?;
    Ok(())
}
