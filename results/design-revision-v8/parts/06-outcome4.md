- **Whether outcome 4 could fire at all** is known at the second freeze
  [r1v5 N5; r2v6 #71; r3v7 R3-2]. Outcome 4 needs two things of one
  negative, and `attain.py` measures, on the null side, whether any negative
  could supply both.
  - **The G condition: 0 < G_j and G_j,hi ≤ G_BM,u,lo.** A unique survivor
    in the core has reach > 0. So the garden must make some targets unique,
    but few enough. G_j,hi ≤ 0.00107 allows **at most 4 targets reached at
    reach 1**, and at most about 8 reach-units however thinly the reach is
    spread. The bound itself is about 11.4 units, and the interval takes the
    rest (2.10) [me: `results/design-revision-v8/outcome4_bound.py`].
    Revision 7 wrote "about 11 reach-units", which was the bound, not what
    it allows. 𝒢_BM* reaches about 18 units, so a negative's garden must be
    at least about four times more selective than 𝒢_BM*. The gardens differ
    in size: 294 readings for AEN-TROY, 90 for ARG-RETURN and 32 for
    QS-SACK, before F5 expansion, against 𝒢_BM*'s 36 (2.6).
  - **The eclipse condition: hit_j(m̂).** Some eclipse-compatible reading of
    𝒢_j has, in one of the two windows above, at their fixed positions, a
    unique survivor whose eclipse has h_tot ≥ m̂, at the eclipse-compatible
    option's own site and day (on the mapped survivors above). It is hit_j
    with m̂ in M_Ody's place. m̂ = 0.304 is the design-stage value of M_Ody
    on the 5-s-grid window (2.3), frozen as its null-side stand-in, because
    M_Ody itself reads the target (4.4). Like every null-side quantity, it
    is computed on the masked pool (4.2).
  - **E_j, reported beside it as context.** E_j is the number of
    conjunctions u of the core with h_tot(u) ≥ m̂, at the option's own site
    and day, that some eclipse-compatible reading makes the unique survivor
    of a 136- or 251-year window containing it, anywhere in the core
    (reach > 0, on the mapped survivors). It says whether a window elsewhere
    could have fired. It is reported at m̂, 0.2 and 0.4.
  - **Why the two windows, and not the core** [r3v7 R3-2]. Revision 7's
    eclipse condition was E_j ≥ 1. But label 4 is scored only in the
    Odyssey's two windows, so an eclipse made unique in another century
    satisfied E_j and could never fire label 4. Q_attain4 could then stay
    silent while label 4 was impossible, and P25 could pass on it.
    hit_j(m̂) asks what label 4 asks, with m̂ for M_Ody. Revision 6 read the
    G condition alone, which a negative could meet while no
    eclipse-compatible reading reaches any eclipse [r2v6 #71]. Revision 5
    had read an even weaker condition, G_BM,u > U0(n_j).
  - **Why it is sound.** M_Ody ≥ m̂ is expected (4.4), and then a hit at
    M_Ody is a hit at m̂, with one exception. The mask hides 16 Apr −1177
    from every null-side search, so a negative whose only hit is that date
    has hit_j after the second freeze and not hit_j(m̂) before it. Masking
    can only add hits elsewhere, by lengthening a neighbour's survivor gap
    (13 row 44). In that case, or if the measured M_Ody fell below m̂,
    label 4 could fire although the null-side record printed Q_attain4. So
    the rule prints Q_attain4 only when label 4 does not fire (9.2), and the
    verdict then says why the record and the label disagree.
  - **Q_attain4** holds if no clean negative meets both conditions. "No
    label 4" then means nothing, and the verdict says so.