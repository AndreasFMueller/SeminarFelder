%
% konvergenz.m
%
% (c) 2025 Prof Dr Andreas Müller
%
n = 10
epsilon = 1e-6

D = -2 * eye(n);
L = circshift(eye(n),1);
L(1,n) = 0;
R = L';

B = inverse(L+D) * R;
rhoGaussSeidel = max(abs(eig(B)))
mGaussSeidel = log(epsilon) / log(rhoGaussSeidel)

C = inverse(D) * (L + R);
rhoJacobi = max(abs(eig(C)))
mJacobi = log(epsilon) / log(rhoJacobi)

