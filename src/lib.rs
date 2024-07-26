use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sha3::{Shake128, digest::{Update, ExtendableOutput, XofReader}};

/// Returns the first n bytes of Shake128 initialized with
/// input_bytes
#[pyfunction]
fn pyo3_shake_128(py: Python, input_bytes: &[u8], n: usize) -> PyObject {
    let mut hasher = Shake128::default();
    hasher.update(input_bytes);
    let mut xof = hasher.finalize_xof();
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
    Ok(())
}
