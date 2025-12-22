"""
Quick test script to verify simulation and inference packages work.
"""

import sys
import numpy as np

print("Testing MQGT-SCF Simulation Package...")
print("=" * 50)

try:
    from mqgt_scf_simulation import MQGT_SCF_Simulator
    
    # Test initialization
    sim = MQGT_SCF_Simulator(variant='A', eta=1e-6)
    print("✓ Simulator initialized (Canon-A)")
    
    # Test QRNG forward model
    result = sim.qrng_forward_model(N_trials=10000, E_0=0.0, E_1=1.0)
    print(f"✓ QRNG forward model: N_0={result['N_0']}, N_1={result['N_1']}")
    print(f"  Test statistic T: {result['T']:.6f}")
    print(f"  Expected T: {result['E_T']:.6f}")
    
    # Test Higgs portal
    h_result = sim.higgs_portal_forward_model(g_phi=1e-3, theta=0.1)
    print(f"✓ Higgs portal forward model: Γ_inv = {h_result['Gamma_inv']:.6e} GeV")
    
    # Test Canon-B
    sim_b = MQGT_SCF_Simulator(variant='B', eta=1e-6, ell_K=1.0)
    print("✓ Simulator initialized (Canon-B)")
    
    # Test kernel
    x1 = np.array([[0.0, 0.0]])
    x2 = np.array([[1.0, 0.0]])
    K = sim_b.kernel_gaussian(x1, x2)
    print(f"✓ Gaussian kernel: K(0,1) = {K[0]:.6f}")
    
    print("\n" + "=" * 50)
    print("Testing MQGT-SCF Inference Package...")
    print("=" * 50)
    
    from mqgt_scf_inference import MQGT_SCF_Inference
    
    inference = MQGT_SCF_Inference(sim)
    inference.set_default_priors()
    print("✓ Inference engine initialized")
    print("✓ Default priors set")
    
    # Add data
    inference.add_channel_data('qrng', {
        'N_0': result['N_0'],
        'N_1': result['N_1'],
        'E_0': 0.0,
        'E_1': 1.0
    })
    print("✓ QRNG data added")
    
    # Test likelihood
    log_likelihood = inference.likelihood_qrng(1e-6, inference.data['qrng'])
    print(f"✓ Likelihood computed: log L = {log_likelihood:.2f}")
    
    # Test posterior
    params = {'eta': 1e-6}
    log_post = inference.log_posterior(params)
    print(f"✓ Posterior computed: log p = {log_post:.2f}")
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED ✓")
    print("=" * 50)
    print("\nPackages are ready for use!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("  pip install numpy scipy matplotlib")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

