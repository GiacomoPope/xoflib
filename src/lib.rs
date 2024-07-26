use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sha3::{Shake128, digest::{Update, ExtendableOutput, XofReader}};

/// Returns the first 10 bytes of Shake128 initialized with
/// b"123"
#[pyfunction]
fn shake_123(py: Python) -> PyObject {
    let mut hasher = Shake128::default();
    hasher.update(b"123");
    let mut xof = hasher.finalize_xof();
    let mut res = [0u8; 10];
    xof.read(&mut res);
    PyBytes::new_bound(py, &res).into()
}

/// A Python module implemented in Rust.
#[pymodule]
fn xof_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(shake_123, m)?)?;
    Ok(())
}
