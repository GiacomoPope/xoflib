use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sha3::{digest::{core_api::XofReaderCoreWrapper, ExtendableOutput, Update, XofReader}, Shake128, Shake128ReaderCore};


// Very silly first attempt at a class

#[pyclass(name="Shake128_pyo3")]
struct Shake128Py {
    xof: XofReaderCoreWrapper<Shake128ReaderCore>
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

    fn read(&mut self, py: Python, n: usize) -> PyObject {
        let mut res = vec![0u8; n];
        self.xof.read(&mut res);
        PyBytes::new_bound(py, &res).into()
    }
}

// Some simple functions used for testing

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128(py: Python, input_bytes: &[u8], n: usize) -> PyObject {
    let mut hasher = Shake128::default();
    hasher.update(input_bytes);
    let mut xof: sha3::digest::core_api::XofReaderCoreWrapper<sha3::Shake128ReaderCore> = hasher.finalize_xof();
    let mut res = vec![0u8; n];
    xof.read(&mut res);
    PyBytes::new_bound(py, &res).into()
}

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128_one_block(py: Python, input_bytes: &[u8]) -> PyObject {
    let mut hasher = Shake128::default();
    hasher.update(input_bytes);
    let mut xof = hasher.finalize_xof();
    let mut res = [0u8; 168];
    xof.read(&mut res);
    PyBytes::new_bound(py, &res).into()
}

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128_n_blocks(py: Python, input_bytes: &[u8], n: usize) -> PyObject {
    let mut hasher = Shake128::default();
    hasher.update(input_bytes);
    let mut xof = hasher.finalize_xof();
    let mut res = vec![0u8; n * 168];
    xof.read(&mut res);
    PyBytes::new_bound(py, &res).into()
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
