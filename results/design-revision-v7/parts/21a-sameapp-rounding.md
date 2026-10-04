**The meaning of `same_apparition`, frozen** [r2v6 N1 fix 1]. Four
projected rows use it: A.1, B.1, I.1 and J.4. Revision 6 listed it as
vocabulary the harness must implement, and never said what it means. On the
recheck's estimate the two natural meanings put ALM-B on either side of the
5% line, so the gate turned on an undefined option (2.6). Its meaning is now
fixed here, in 10.3 and in `operational_map.json`:

- **visible on Day 0**: the body is on the row's side of the Sun, and its
  rise lead (morning) or set lag (evening) is at least the row's
  `visible_only` minimum at the regime's value, which is 30 min in both
  regimes;
- **the apparition** is the interval between the two geocentric conjunctions
  of the body with the Sun, in apparent ecliptic longitude, that bracket the
  record's instant;
- **the order**: the greatest elongation on the row's side, from the true Sun
  (the event of `ge_true_k`), lies in that interval, after the record's
  instant ("not yet reached": A.1, I.1) or before it ("already past": B.1,
  J.4).

**Why visibility belongs to it.** The reasons come from the text and from
the file, not from the gate:

- an apparition is, in standard usage, a period of visibility;
- every row that carries the option records a sighting of the body on that
  day;
- the file calls `visible_only` the same row's "minimal reading", so its
  literal reading cannot pass a day that the minimal reading fails.

**The history, and the other meaning.** The meaning was fixed after the
recheck's null-side estimate had shown what it does to ALM-B, and with the
truth-side facts of [AppT 2] known. So the other meaning, "on that side of the
Sun" without visibility, is scored on every leg of gate 3b and reported
(seen_ALM_SL_side). It enters no label, but Q_score prints when it would
change the gate's decision. What the frozen meaning does at the truths is in
[AppT 2].

**The rounding step of every ceiling is a frozen family** [r2v6 N6].
Revision 4 rounded regime SL's day ceilings up to the next whole day, and
revision 6 rounded the held-out ceilings up to the next 0.1°. Both steps were
chosen with the slack table in view [r2v6 N6]; what each step does at the
truths is in [AppT 2b]. So every leave-one-set-out ceiling is computed at
three steps:

| step | degrees | days |
|---|---|---|
| fine | up to the next 0.01° | up to the next 0.1 d |
| mid | up to the next 0.05° | up to the next 0.5 d |
| coarse | up to the next 0.1° (revision 6's rule) | up to the next whole day (revision 4's rule) |

Gate 3b and Q_H take their decisions against the claim across the three
steps, as gate 3a takes its decision across its legs. A finer step narrows a
tolerance: that narrows the projection, which helps a set to be seen, and it
can lose a truth, which hurts. So the direction is not known in advance, and
the family covers both. The coarse step is reported first.

