import numpy as np
import os

root = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_Markov"  # set to your experiment folder if needed

paths = {
    "true":  os.path.join(root, "test_true_with_history.npy"),
    "pred":  os.path.join(root, "test_pred_with_history.npy"),
    "state": os.path.join(root, "test_true_state.npy"),
    "metrics": os.path.join(root, "test_metrics.npy"),
}

for k,p in paths.items():
    print(k, "exists:", os.path.exists(p), "|", p)

true = np.load(paths["true"])
pred = np.load(paths["pred"])
state = np.load(paths["state"])
metrics = np.load(paths["metrics"], allow_pickle=True)

def info(name, arr):
    arr = np.asarray(arr)
    print(f"\n[{name}]")
    print(" shape:", arr.shape)
    print(" dtype:", arr.dtype)
    if arr.dtype != object:
        print(" finite:", np.isfinite(arr).all())
        print(" min/max:", np.nanmin(arr), np.nanmax(arr))

info("true_with_history", true)
info("pred_with_history", pred)
info("true_state", state)
print("\n[metrics] type:", type(metrics), "dtype:", getattr(metrics, "dtype", None), "shape:", getattr(metrics, "shape", None))


#Shape Alignment Check 
SEQ_LEN = 50
PRED_LEN = 100
TOTAL = SEQ_LEN + PRED_LEN

# 1) true and pred must have identical shapes
assert true.shape == pred.shape, f"Shape mismatch: true {true.shape} vs pred {pred.shape}"

# 2) find the time dimension (it should equal TOTAL for with_history arrays)
time_dims = [d for d in range(true.ndim) if true.shape[d] == TOTAL]
print("candidate time dims where length==150:", time_dims)

if len(time_dims) == 0:
    raise ValueError(f"No dimension equals TOTAL={TOTAL}. Your saved arrays may not include full history+future.")

# assume last dim is time if ambiguous (common), else pick the first match
t_dim = time_dims[-1]
print("using time dim =", t_dim)

# 3) state length must match number of time steps *in the same unit*
# state could be (N, TOTAL) or (N, TOTAL, 1) or flattened.
print("state shape:", state.shape)

# Try to align state to have time axis = TOTAL too
state_time_dims = [d for d in range(state.ndim) if state.shape[d] == TOTAL]
print("candidate state time dims:", state_time_dims)


#Shape Alignment check 
SEQ_LEN = 50
PRED_LEN = 100
TOTAL = SEQ_LEN + PRED_LEN

# 1) true and pred must have identical shapes
assert true.shape == pred.shape, f"Shape mismatch: true {true.shape} vs pred {pred.shape}"

# 2) find the time dimension (it should equal TOTAL for with_history arrays)
time_dims = [d for d in range(true.ndim) if true.shape[d] == TOTAL]
print("candidate time dims where length==150:", time_dims)

if len(time_dims) == 0:
    raise ValueError(f"No dimension equals TOTAL={TOTAL}. Your saved arrays may not include full history+future.")

# assume last dim is time if ambiguous (common), else pick the first match
t_dim = time_dims[-1]
print("using time dim =", t_dim)

# 3) state length must match number of time steps *in the same unit*
# state could be (N, TOTAL) or (N, TOTAL, 1) or flattened.
print("state shape:", state.shape)

# Try to align state to have time axis = TOTAL too
state_time_dims = [d for d in range(state.ndim) if state.shape[d] == TOTAL]
print("candidate state time dims:", state_time_dims)


u = np.unique(state)
print("unique states (first 20):", u[:20], "| count:", len(u))

# quick check for binary-ish
if len(u) <= 10:
    print("all states:", u)

# check if it's 0/1 or 1/2
if set(u.tolist()) <= {0,1}:
    print("state looks binary 0/1 ✅")
elif set(u.tolist()) <= {1,2}:
    print("state looks binary 1/2 (will map to 0/1 later) ✅")
else:
    print("state is not simple binary. Could be multi-state or not discrete ❌")

 # (N, 100, 1)
print("raw:", state.shape, state.dtype)

state = state.squeeze(-1)                        # (N, 100)
print("squeezed:", state.shape, state.dtype)

# sanity
print("unique:", np.unique(state))

# transition rate within each sequence (future only)
trans_rate = (state[:, 1:] != state[:, :-1]).mean(axis=1)

print("transition rate mean:", float(trans_rate.mean()))
print("transition rate median:", float(np.median(trans_rate)))
print("transition rate min/max:", float(trans_rate.min()), float(trans_rate.max()))
print("any nan?", np.isnan(trans_rate).any())