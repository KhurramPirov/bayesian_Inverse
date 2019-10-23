"""
A very simple test for the ELBO.

Author:
    Ilias Bilionis

Date:
    6/5/2014
    9/17/2014

"""


import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from vuq import MultivariateNormal
from vuq import MixtureOfMultivariateNormals
from vuq import FirstOrderEntropyApproximation
from vuq import EntropyLowerBound
from vuq import ThirdOrderExpectationFunctional
from vuq import EvidenceLowerBound


# Number of dimensions
num_dim = 1

# The number of components to use for the mixture
num_comp = 1

# The (hypothetical) joint distribution
log_p = MultivariateNormal(np.zeros((num_dim, 1)))
log_p.C = [[0.1]]
print ('Target:')
print (str(log_p))

# The approximating distribution
log_q = MixtureOfMultivariateNormals.create(num_dim, num_comp)
print ('Initial:')
print (log_q)

# Pick an entropy approximation
entropy = FirstOrderEntropyApproximation()
entropy_lb = EntropyLowerBound()
# Pick an approximation for the expectation of the joint
expectation_functional = ThirdOrderExpectationFunctional(log_p)
# Build the ELBO
elbo = EvidenceLowerBound(entropy, expectation_functional)
elbo_2 = EvidenceLowerBound(entropy_lb, expectation_functional)
print ('ELBO:')
print (str(elbo))

# Evaluate the elbo
state = (elbo(log_q))
print (state)

# Plot the elbo as a function of mu
mus = np.linspace(-2, 2, 100)
L = []
S = []
F = []
L2 = []
S2 = []
for mu in mus:
    log_q.comp[0].mu = [mu]
    state = elbo(log_q)
    L.append(state['L'])
    S.append(state['S_state']['S'])
    F.append(state['F_state']['F'])
    state_2 = elbo_2(log_q)
    L2.append(state_2['L'])
    S2.append(state_2['S_state']['S'])
L = np.hstack(L)
S = np.hstack(S)
F = np.hstack(F)
L2 = np.hstack(L2)
S2 = np.hstack(S2)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(mus, L2, linewidth=2)
ax.plot(mus, S2, linewidth=2)
ax.plot(mus, F, linewidth=2)
#ax.plot(mus, S2, linewidth=2)
#ax.plot(mus, L2, linewidth=2)
leg = ax.legend(['ELBO', 'Entropy', 'Expectation'], loc='best')
plt.setp(leg.get_texts(), fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=16)
plt.setp(ax.get_yticklabels(), fontsize=16)
ax.set_xlabel('$\mu$', fontsize=16)
png_file = os.path.join('figures', 'test_elbo_1_varying_mu.png')
print ('writing:', png_file)
plt.savefig(png_file)


# Now fix mu and vary C
log_q.comp[0].mu = [0]
Cs = np.linspace(0.05, 0.15, 100)
L = []
S = []
F = []
L2 = []
S2 = []
for C in Cs:
    log_q.comp[0].C = [[C]]
    state = elbo(log_q)
    L.append(state['L'])
    S.append(state['S_state']['S'])
    F.append(state['F_state']['F'])
    state_2 = elbo_2(log_q)
    L2.append(state_2['L'])
    S2.append(state_2['S_state']['S'])
L = np.hstack(L)
S = np.hstack(S)
F = np.hstack(F)
L2 = np.hstack(L2)
S2 = np.hstack(S2)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(Cs, L2, linewidth=2)
ax.plot(Cs, S2, linewidth=2)
ax.plot(Cs, F, linewidth=2)
#ax.plot(Cs, L2, linewidth=2)
#ax.plot(Cs, S2, linewidth=2)
leg = ax.legend(['ELBO', 'Entropy', 'Expectation'], loc='best')
plt.setp(leg.get_texts(), fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=16)
plt.setp(ax.get_yticklabels(), fontsize=16)
ax.set_xlabel('$C$', fontsize=16)
png_file = os.path.join('figures', 'test_elbo_1_varying_C.png')
print ('writing:', png_file)
plt.savefig(png_file)

# Now do a contour plot
mus = np.linspace(-1, 1, 64)
Cs = np.linspace(0.01, 0.5, 64)
Mus, CCs = np.meshgrid(mus, Cs)
Z = np.zeros(Mus.shape)
for i in range(Z.shape[0]):
    for j in range(Z.shape[1]):
        log_q.comp[0].mu = [Mus[i, j]]
        log_q.comp[0].C = [[CCs[i, j]]]
        state = elbo_2(log_q)
        Z[i, j] = state['L']
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.contourf(Mus, CCs, Z)
ax.plot([log_p.mu[0]], [log_p.C[0, 0]], 'ok', markersize=16)
ax.set_xlabel('$\mu$', fontsize=16)
ax.set_ylabel('$C$', fontsize=16)
ax.set_title('ELBO as a function of $\mu$ and $C$', fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=16)
plt.setp(ax.get_yticklabels(), fontsize=16)
cbar = fig.colorbar(cax)
plt.setp(cbar.ax.get_xticklabels(), fontsize=16)
png_file = os.path.join('figures', 'test_elbo_1_varying_both.png')
print ('writing:', png_file)
plt.savefig(png_file)
