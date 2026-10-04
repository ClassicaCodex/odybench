### 4.2 Candidate pools and target pools (Ithaki unless a rule names another site)

**Candidate pools.**

- **P_all** holds every geocentric apparent-longitude conjunction, computed
  with DE431 in yearly chunks and SMH2020 ΔT for UT. Each candidate carries
  **one Day-0 date per clock**: `day0_jdn_ut2` (B&M's clock; F2 (a)) and
  `day0_jdn_lmt` (F2 (b), the negatives, R_anc) [r1 N12].
- **P_day** holds the conjunctions whose instant falls in daylight at the
  site (Sun's centre above −0.8333°). At Ithaca that is 50.9% of them [vis
  §4.2], and only these can give a visible solar eclipse.
- **P_spring** holds the conjunctions passing C_rel (4.5) on the sequential
  or the parallel count, with Day 0 the UT+2 date. The slots below use the
  same Day 0 and the same count, so that the identity at the end of this
  section is exact.
- **P_BM** holds the candidates of P_all, over the whole background, that
  pass at least one reading of 𝒢_BM*. It is the null pool of the held-out
  test (section 7).

**The masked target.** In the null-side stage (12.3) every pool is built
without 16 Apr −1177. `pools.targets(..., mask_target=True)` removes it
before any predicate is evaluated, and `clues.evaluate` raises if asked to
evaluate it (I13(g)).

**Target pools.** Section 5.3 says which pool each G uses, and why.

| pool | definition | size in the core (estimate, 2.9) |
|---|---|---|
| T | P_day ∩ core | about 10,690 |
| T_C | T ∩ P_spring | 892 |
| T_A(v) | the targets in T_C whose sky satisfies the Venus slot and the Mercury slot of variant v, on the same day count as C | 56–131 by variant (table below) |

**The slot family** (`data/prereg/slots.json`) [r2 R2-2]. A slot defines the
*categorical* reading that the record shows was formed with the target in
view (5.3). The recheck showed that the slot definition sets G_BM through
1/n_A. Nothing in the record fixes a width, so the bench freezes a family and
uses it against the claim being made.

| key | Venus slot (Day −5 seq, −4 par) | Mercury slot (Day −34 seq, −33 par) | source | n_A (2.9) |
|---|---|---|---|---|
| v0, documented | Venus rises before the Sun, with the Sun at or below −7° at Venus' rising (a visible morning star, AV 7°) | Mercury within 6.0 d (continuous) of a morning rise-azimuth maximum (vertex, 4.3), a greatest western elongation, or a morning station, **and** visible (Sun at or below −10° at Mercury's rising) | V: MacDonald identifies the herald as Venus, the morning star of that spring [unread §2.1, §2.5], with de Jong's AV [vis §1.2]. M: B&M name the three events and require Mercury visible [B&M §References]; 6 d is the slack of Ptolemy's Mercury records, all 14 within 5.5 d [alm §4] | 82 |
| v1, revision 3 | as v0 | event within 6.0 d, **or** visible | [v3 §4.2] | 131 |
| v2 | as v0 | event within 6.0 d | | 87 |
| v3 | as v0 | event within 4.0 d (12 of the 14 *Almagest* records) | [alm §4] | 66 |
| v4 | Venus rises at least 60 min before the Sun | as v1 | the FULL-tier herald threshold [vis §1.3] | 101 |
| v5 | as v4 | as v3 | | 56 |

- **Pairing of the day counts** [r2 R2-2]. C, the Venus slot and the Mercury
  slot hold on one count: either the sequential count (−29/−12, −5, −34) or
  the parallel count (−28/−11, −4, −33). A target is in T_A(v) if either
  count passes as a whole. Revision 3's "either day count" let Day −5 mix
  with Day −33; that is withdrawn.
- **"Near greatest elongation" is not MacDonald's wording.** Revision 3
  wrote that MacDonald puts Venus "near morning elongation" [v3 §5.3], and
  the recheck took that as his categorical reading [r2 R2-2].
  - His p. 327 dates the greatest morning elongation, 17 March, and says no
    more [unread §2.1].
  - On 11 Apr −1177 Venus stood 44.3° west of the Sun. That was 1.84° below
    the apparition's maximum of 46.14°, and 26 days after it [unread §2.5].
  - A Venus slot narrower than that would exclude MacDonald's own case.
  - The variant "western elongation within 2° of the apparition's maximum"
    (v6) is reported. It is not in the rule family, because its width is set
    by the target's own value.
- **How the family is used.**
  - Label 2's G leg and Q_tol take the variant most favourable to B&M, the
    smallest G_BM,lo.
  - Q_slot is printed when a decision differs between variants.
  - The held-out test does not use T_A (section 7), so outcome 1 does not
    depend on the slots.

**One identity follows.** Every reading of 𝒢_BM* requires three things:

- C;
- a Venus lead of at least 90 min. That implies the Venus slots of every
  variant: at Ithaca's latitude the Sun sinks at least about 0.15° a minute
  near the horizon, so a 90-min lead puts it below −13° when Venus rises
  [me];
- a morning Mercury event within 3.5 d. That implies the Mercury slots of v1
  to v5.

So no target outside T_A(v) is ever reached, for v1 to v5, and

  G(𝒢_BM*, T) = (n_A(v) / n_T) · G(𝒢_BM*, T_A(v)) = G_BM,u

exactly, the same number for every such v. For v0 the visibility part is not
implied by the readings with visibility off. The recheck found no reached
target outside T_A(v0) [r2 R2-2], and the bench reports that count. I9(c)
checks the identity in the code, and I14 uses it as a realisability
constraint (9.4).

