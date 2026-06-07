# Proof: Dual of the Dual is the Primal

Consider a linear program in the following form (primal):

\[
\begin{array}{ll}
\max & c^\top x \\
\text{s.t.} & Ax \le b \\
            & x \ge 0
\end{array}
\tag{P}
\]

where \(A \in \mathbb{R}^{m \times n}\), \(b \in \mathbb{R}^m\), \(c \in \mathbb{R}^n\).

---

## Step 1: Write the Dual of (P)

The dual of a maximization problem with \(\le\) constraints and nonnegative variables is a minimization problem with \(\ge\) constraints and nonnegative dual variables:

\[
\begin{array}{ll}
\min & b^\top y \\
\text{s.t.} & A^\top y \ge c \\
            & y \ge 0
\end{array}
\tag{D}
\]

---

## Step 2: Write the Dual of (D)

Now treat (D) as the "primal" for the purpose of forming its dual.  
(D) is a minimization problem with \(\ge\) constraints and nonnegative variables.  
To apply the standard duality rules, we first convert (D) to a maximization form.

### Convert (D) to a maximization problem

Multiply the objective by \(-1\) (changing min to max) and reverse the inequality direction:

\[
\begin{array}{ll}
\max & -b^\top y \\
\text{s.t.} & -A^\top y \le -c \\
            & y \ge 0
\end{array}
\tag{D'}
\]

Now (D') has the form: maximization with \(\le\) constraints and nonnegative variables, exactly matching the primal form we started with.

### Apply duality rules to (D')

For a problem of the form

\[
\begin{array}{ll}
\max & \tilde{c}^\top \tilde{x} \\
\text{s.t.} & \tilde{A} \tilde{x} \le \tilde{b} \\
            & \tilde{x} \ge 0
\end{array}
\]

its dual is

\[
\begin{array}{ll}
\min & \tilde{b}^\top \tilde{y} \\
\text{s.t.} & \tilde{A}^\top \tilde{y} \ge \tilde{c} \\
            & \tilde{y} \ge 0
\end{array}
\]

Identify the components of (D'):

- \(\tilde{x} = y\)
- \(\tilde{c} = -b\)
- \(\tilde{A} = -A^\top\)
- \(\tilde{b} = -c\)

Now form the dual of (D'):

\[
\begin{array}{ll}
\min & \tilde{b}^\top \tilde{y} \\
\text{s.t.} & \tilde{A}^\top \tilde{y} \ge \tilde{c} \\
            & \tilde{y} \ge 0
\end{array}
\]

Substitute:

\[
\begin{array}{ll}
\min & (-c)^\top \tilde{y} \\
\text{s.t.} & (-A^\top)^\top \tilde{y} \ge -b \\
            & \tilde{y} \ge 0
\end{array}
\]

Simplify:

- \((-c)^\top \tilde{y} = -c^\top \tilde{y}\)
- \((-A^\top)^\top = -A\) because \((A^\top)^\top = A\) and the minus sign remains.

Thus we have:

\[
\begin{array}{ll}
\min & -c^\top \tilde{y} \\
\text{s.t.} & -A \tilde{y} \ge -b \\
            & \tilde{y} \ge 0
\end{array}
\]

Multiply the objective and the constraint by \(-1\) (which turns the min back to max and flips the \(\ge\) to \(\le\)):

\[
\begin{array}{ll}
\max & c^\top \tilde{y} \\
\text{s.t.} & A \tilde{y} \le b \\
            & \tilde{y} \ge 0
\end{array}
\]

Rename \(\tilde{y}\) to \(x\) (since it is just a dummy variable). This yields exactly the original primal problem (P):

\[
\begin{array}{ll}
\max & c^\top x \\
\text{s.t.} & A x \le b \\
            & x \ge 0
\end{array}
\]

---

## Conclusion

We have shown that the dual of the dual linear program returns the original primal linear program. Hence, for any linear program (in the given form), **the dual of the dual is the primal**.

\[
\boxed{\text{Dual of Dual} = \text{Primal}}
\]