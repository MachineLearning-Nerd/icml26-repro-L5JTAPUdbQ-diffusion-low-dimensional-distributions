# Claim 1 threshold-escape method

For the Rademacher target, every training point is `+1` or `-1`. At forward
time `T=log n`, define

`b=[1+sqrt(2(n^2-1) log(N/log N))]/n`.

If the VE coordinate `z>nb`, every KDE kernel is below the paper's threshold,
regardless of the observed signs, so the estimated score is exactly zero.

On the event `Y0>b+1` and `min M_r>=-1`, where
`M_r=sqrt(2) integral_0^r exp(-u)dB_u`, the zero-score reverse SDE has the exact
integrating-factor solution `Y_r=exp(r)(Y0+M_r)`. Its VE coordinate is
`z_r=n(Y0+M_r)>nb`. Since the smoothing variance only decreases, the threshold
condition persists for the whole path. At output, the sample is at least
`n exp(-tau)b` while the target is supported on `{-1,+1}`.

The event probability is bounded below using the Gaussian tail and reflection
principle. Mills' ratio then gives
`log W1 >= -2 sqrt(2 log n)-O(log log n)`, which is asymptotically larger than
the claimed `n^-1/2` times any fixed polylogarithm.
