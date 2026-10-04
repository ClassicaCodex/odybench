# The Odyssey's internal chronology, from Hermes' trip (5.1) to the slaughter (book 22)

odybench research note. Written 2026-10-03 by Claude for the odybench workflow.
Scope: rebuild the day-by-day chronology from the **Greek** text, and give the day offsets that Baikouzis & Magnasco (B&M, PNAS 105 (2008) 8823-8828) use for Hermes (read as Mercury), the Pleiades and Boötes (read as the season), the morning star at Ithaca (read as Venus) and the slaughter (Day 0, read as the new moon and the eclipse). For each offset I give B&M's value, the smallest and largest values the text allows, and the reading behind each.

Tags used in this note:
- **[text]**: what the Greek says, cited as book.line from `data/text/odyssey-grc.tsv` (Perseus). Murray (`odyssey-murray.tsv`) and Butler (`odyssey-butler.tsv`) were used only to check my reading.
- **[B&M]**: B&M 2008, main text (PMC2440358, read in full).
- **[B&M SI]**: their Supporting Information. I read its text layer from `data/bm2008-a/baikouzis-magnasco-2008-SI.pdf`, which a sibling agent got from a Wayback capture.
- **[schol.]**: Dindorf's scholia, `data/text/scholia-odyssey-grc.tsv`.
- **[me]**: my own inference or arithmetic. It was computed with Python 3.14, using scratchpad scripts that grep dawn and nightfall formulas and convert Julian dates to JD.
- Secondary reports are labelled as such. Section 8 lists what I could not read.

---

## 0. Bottom line

1. **What B&M's paper actually uses differs from what is commonly reported.**
   - The search in the paper applies its constraints at T<sub>i</sub>−34 (Mercury), T<sub>i</sub>−29 (Pleiades and Boötes), T<sub>i</sub>−5 (Venus) and T<sub>i</sub>−11 (Poseidon and the equinox, listed but not applied). These are the "sequential" column of their Table 1 [B&M *Method*, *Intersecting the Constraints*].
   - Their "parallel" column gives −33, −28, −4 and −10 [B&M Table 1].
   - The popular triple "Mercury 33, Pleiades 29, Venus 6" comes from the Rockefeller University press release of 23 June 2008 (also on EurekAlert). It matches **neither** column, and no single counting convention produces it (§2.3).
2. **The text fixes most of the chain. Only two joints are genuinely open, plus one minority reading.**
   - Hermes' day H to departure D is 5 days (5.228, 5.262-263). It is 4 only if one counts inclusively from Hermes' day.
   - D to the storm on the 18th day (Σ) is 17 or 18 days. It depends on whether the departure day is the first of the "17 days" (5.278-279). The text never says when in the day he left.
   - Σ to the landing on Scheria (L) is **2**. This is forced: 5.388-390 together with 6.170 ("yesterday, on the twentieth day") and 5.34 (Zeus: "on the twentieth day").
   - L to the Ithaca arrival (I) is **4**. This is firm, from explicit dawns at 6.48, 8.1, 13.18 and 13.93-95.
   - I to the slaughter (S) is 4 or 5. It depends on whether Athena's night visit to Telemachus in Sparta (15.1-8) falls on the night before Odysseus reaches Ithaca or the night after.
3. **Defensible offsets before the slaughter** (S − X in calendar days) [me]:
   - Mercury (H): **32-34**, or **31** if the raft days are counted inclusively from Hermes' day. B&M use 34.
   - First raft night (D, evening): **27-29**. B&M use 29.
   - Any raft night: **11-29**. The Pleiades passage describes every night of the voyage (§4.I).
   - Venus (I, pre-dawn): **4-5**. B&M use 5.
   - Poseidon's storm (Σ): **10-11**. B&M use 11.
   - B&M took the **maximum** at both open joints.
4. **Published chronologies disagree in exactly these places.**

   | Chronology | Days in the poem | H | D | I | S | Offsets M / P / V |
   |---|---|---|---|---|---|---|
   | de Jong 2001 (= Delebecque 1958, Hellwig 1964, Apthorp 1980; Monro on 13.18 and 13.93, as quoted) | 41 | 7 | 12 | 35 | 40 | 33 / 28 / 5 |
   | Stanford 1959, as tabulated by Struck | 40 | 7 | 12 | 35 | 39 | 32 / 27 / 4 |
   | B&M sequential | 42 | 7 | 12 | 36 | 41 | 34 / 29 / 5 |
   | B&M parallel | n/a | | | | | 33 / 28 / 4 |

   B&M's sequential count is de Jong's count plus **one day inserted after the departure from Ogygia**. B&M say Odysseus left at sunset, which the text does not state.
5. **Errors and inconsistencies inside B&M that matter for the chronology:**
   - (a) They put the moonless night of 14.457 on "Night −2", but their own Table 1 puts book 14 on Day −5 (−4 parallel). The sibling agent's notes (`docs/research-bm2008-a.md`, `-b.md`) found this independently.
   - (b) Their SI Table S1 dates Hermes' visit to **15 March**. Their main text gives **13 March** (T<sub>i</sub>−34).
   - (c) They say Calypso told Odysseus to watch the Pleiades and Boötes. In the text her instruction concerns only the Bear (5.276-277).
6. **Theoclymenus speaks on the slaughter day itself.** This is S, the festival of Apollo. He speaks at the meal (δεῖπνον, 20.390-394), after the dawn at 20.91 and the public hecatomb in Apollo's grove (20.276-278). The text gives no clock time; "noon" is B&M's inference.
7. **Only one ancient day number survives in Dindorf's scholia.** The alternative argument to book 8 (MSS H, P, Q) calls the Phaeacian assembly day "Day 23" (Ἡμέρα τρίτη καὶ εἰκοστή). Its starting point is unstated. If it counts from the day Odysseus left Ogygia, it implies B&M's 20-day departure-to-landing interval, not de Jong's 19 (§6.1).

---

## 1. Conventions

- **Day boundaries.** A Homeric narrative day runs from one dawn formula to the next. I label each night by the evening that begins it: "night of X" is the night from X into X+1.
- **Offsets.** An offset is the difference of calendar dates, S − X, where S is the slaughter day. B&M's "Day −n" is the same measure.
  - An *inclusive* count adds 1 ("on the sixth day" for a difference of 5).
  - An *exclusive* count subtracts 1 (days strictly between).
- **Calendar and time scales** (B&M's choices, which I keep):
  - Proleptic Julian calendar.
  - B&M's Day 0 is **16 April 1178 BC = astronomical year −1177, JD 1291264** at noon [me: standard Julian-calendar JD algorithm].
  - B&M give times as "local to the Greek islands" and do not say whether that is local mean or local apparent solar time [B&M *Method*]. Their ΔT for the eclipse is 27,602.7 s (Starry Night Pro) [B&M *Method*]. Their SI also cites 28,907 s and 28,590 s for other tracks and canons [B&M SI Fig. S1].
  - The phenomena belong to different parts of the day: Pleiades and Boötes at evening nautical twilight (B&M Fig. 2: 18 March, 7:38 pm); Venus before sunrise on I; Mercury at dawn on H; the eclipse near local noon (B&M Fig. 1: 12:02 pm).
- **Dates implied by each offset** if Day 0 is 16 April −1177 (Julian) [me]:

  | Offset | Date |
  |---|---|
  | 34 | 13 Mar |
  | 33 | 14 Mar |
  | 32 | 15 Mar |
  | 31 | 16 Mar |
  | 29 | 18 Mar |
  | 28 | 19 Mar |
  | 27 | 20 Mar |
  | 12 | 4 Apr |
  | 11 | 5 Apr |
  | 10 | 6 Apr |
  | 9 | 7 Apr |
  | 8 | 8 Apr |
  | 5 | 11 Apr |
  | 4 | 12 Apr |

---

## 2. What B&M actually did

### 2.1 Their Table 1 [B&M Table 1, quoted in substance]

| Event | Sequential | Parallel |
|---|---|---|
| Council 1 | −40 | −33 |
| Ithaca assembly | −39 | −32 |
| **Council 2 / Hermes** | **−34** | −33 |
| Raft | −33 to −30 | −32 to −29 |
| **Departure "at sunset"** | **−29** | −28 |
| Sailing | −28 to −12 | −27 to −11 |
| **Poseidon sinks raft** | **−11** | −10 |
| Swimming | −10 | −9 |
| Lands on Scheria | −9 | −8 |
| Nausicaa | −8 | −7 |
| Palace, games, tales | −7 | −6 |
| Gifts, boards at sunset | −6 | −5 |
| **Ithaca "with the Star of Dawn"** | **−5** | −4 |
| Athena fetches Telemachus | −4 | −4 |
| Telemachus travels; Odysseus dines with Eumaeus | −3 | −3 |
| Telemachus reaches Ithaca | −2 | −2 |
| Odysseus enters the hall | −1 | −1 |
| **Festival, eclipse, slaughter** | **0** | 0 |
| Laertes | +1 | +1 |

- Their note says the sequential reckoning makes "the day Odysseus lands in Ithaca and the day Athena tells Telemachus to return from Sparta" consecutive days. The parallel reckoning has Athena arrive in Sparta "instantaneously". They also note: departure near sunset plus landing before sunset gives "exactly 20 days and 20 nights at sea".
- They cite no Homeric chronology for this table. The only reference attached to it is Schoch 1926 (ref. 13), for the rule that simultaneous events are narrated as consecutive. Page 1955 (ref. 10) is cited elsewhere, and only for suspicion of the Theoclymenus lines.
- The **search** uses the sequential offsets. The text requires the constellations "on T<sub>i</sub>−29", Venus to rise at least 90 minutes before the Sun "on T<sub>i</sub>−5", and Mercury near its westernmost rise azimuth "on T<sub>i</sub>−34". It lists T<sub>i</sub>−11 for the equinox [B&M *Method*, *References and Constraints*].
- For 1178 BC the dates are: T<sub>i</sub>−34 = 13 March; T<sub>i</sub>−29 = 18 March; T<sub>i</sub>−11 = 5 April; T<sub>i</sub>−5 = 11 April [B&M *Intersecting*]. I checked these against the Julian calendar.
- They claim the date works "both under parallel and under consecutive chronologies, and exactly so under the latter" [B&M *Intersecting*].

### 2.2 Problems inside B&M that concern the chronology

- **(a) The moonless night.** B&M: "Night −2 is dark and moonless (xiv.457)" [B&M *Method*]. But Table 1 puts xiii.93-xiv.533 on Day −5 (seq) or −4 (par).
  - Under any reading, 14.457 is the night of Odysseus' first evening at Eumaeus' hut, so the night of I. That is S−5 (seq) or S−4 (par), never −2 [me; text 14.407, 14.457, 14.523-533].
  - This matters for the lunar test. A night 4-5 days before conjunction has a waning crescent rising in the small hours. A night 2 days before is genuinely moonless.
- **(b) Hermes' date.** SI Table S1 glosses v.225 as "March 15, the day of Hermes visit, almost new moon" [B&M SI p. 4]. The main text puts Hermes on T<sub>i</sub>−34 = 13 March. 15 March is T<sub>i</sub>−32, which is Stanford's count, not theirs.
- **(c) Calypso's instruction.** Table 1 says Calypso sends him off "telling him to watch Pleiades and Boötes and keep the Bear left". In the Greek, τήν in 5.276 picks up Ἄρκτον (5.273): Calypso's instruction is only to keep **the Bear** on his left (5.276-277) [text]. The star-gazing in 5.271-272 is his own.
- **(d) The sunset departure.** "Sets sail at sunset" is not in the text. 5.263-269 gives no time of day [text]. It is the hinge of their 20-day count (§4.B).
- **(e) Moon phase at departure.** The main text says the night of T<sub>i</sub>−29 "is New Moon". The SI says "the previous full moon is when Odysseus 'gladly spread his sails'" [B&M SI p. 1]. One of the two is a slip. The main text's statement fits a lunation of about 29.5 days before 16 April [me].
- **(f) The Pleiades' last night.** B&M give the Pleiades' last evening visibility as 3 April in one place [B&M *References*] and 4 April in another [B&M *Intersecting*].
  - Under their own **parallel** column the last raft night is the evening of −11 = 5 April. That is one or two nights after the Pleiades' last visibility by their own figures.
  - So the claim that the date works "both" ways rests on the stated "uncertainty of at least a day" [me, from B&M's numbers].

### 2.3 Where "33 / 29 / 6" comes from

- The Rockefeller press release (23 June 2008; the EurekAlert copy is identical) says:
  - "six days before the slaughter, Venus is visible and high in the sky";
  - "twenty-nine days before", the Pleiades and Boötes are visible together at sunset;
  - "33 days before", Mercury is high at dawn.
- Neither column of the paper gives this triple. Possible derivations [me]:
  - **33.** B&M parallel (−33), or de Jong's classic count (Day 7 to Day 40), or B&M's sequential −34 counted *exclusively*.
  - **29.** B&M sequential (−29), or de Jong's 28-day difference counted *inclusively*.
  - **6.** B&M's −5 counted *inclusively* (I and S both counted). It could also come from labelling the pre-dawn of I by the evening that began that night, the night of I−1 = −6 seq. A literal 6-day *difference* needs Athena to reach Sparta only on the second night after leaving Ithaca. Nothing in the text supports that (§4.F).
- So the triple mixes conventions under any derivation. The only consistent triples are those in §5.

---

## 3. Day by day from the Greek

The columns give de Jong's day number (dJ), B&M's sequential and parallel offsets, the event, and the dawn and nightfall lines. "—" means the text marks no dawn or nightfall for that day; the day is only counted.

### 3.1 Odysseus: Ogygia, raft, Scheria

| Day | dJ | B&M seq / par | Event [text] | Dawn | Nightfall |
|---|---|---|---|---|---|
| **H** | 7 | −34 / −33 | Second council (5.3-42); Hermes flies to Ogygia, talks with Calypso, leaves (5.43-148); Calypso tells Odysseus (5.149-224); they sleep together (5.226-227). Zeus forecasts landfall "on the twentieth day" (5.34). | 5.1-2 Ἠὼς δ' ἐκ λεχέων παρ' ἀγαυοῦ Τιθωνοῖο | 5.225 ἠέλιος δ' ἄρ' ἔδυ καὶ ἐπὶ κνέφας ἦλθεν |
| H+1 | 8 | −33 / −32 | Tools handed over, trees felled; the raft is begun (5.228-261, summarized). | 5.228 ἦμος δ' ἠριγένεια φάνη ῥοδοδάκτυλος Ἠώς | — |
| H+2, H+3 | 9-10 | −32, −31 | Building (summarized). | — | — |
| H+4 | 11 | −30 / −29 | "It was the fourth day, and on it all was finished" (5.262). | counted (τέτρατον ἦμαρ) | — |
| **D** = H+5 | 12 | −29 / −28 | "On the fifth she sent him from the island": bath, clothes, provisions, wind (5.263-268). He spreads sail (5.269). Time of day not stated. | counted (τῷ δ' ἄρα πέμπτῳ) | — |
| voyage | 12-28 | −28..−12 / −27..−11 | He steers and does not sleep, watching the Pleiades, Boötes and the Bear (5.270-277, imperfects); "17 days he sailed" (5.278). | — | — |
| **Σ** (18th day) | 29 | −11 / −10 | Mountains of the Phaeacians appear (5.279-281); Poseidon, back from the Ethiopians, raises the storm (5.282-296); wreck; Ino (5.333-353); Poseidon leaves (5.380-381); Athena calms all winds but Boreas (5.382-387). | counted (ὀκτωκαιδεκάτῃ, 5.279) | 5.294 ὀρώρει δ' οὐρανόθεν νύξ: storm darkness, not a sunset formula |
| Σ+1 | 30 | −10 / −9 | Adrift: "two nights and two days" (5.388-389). | — | — |
| **L** = Σ+2 | 31 | −9 / −8 | "When Dawn completed the third day" the wind drops and he sees land (5.390-393); swims to a river mouth (5.438-453); beds down in leaves (5.474-493). | 5.390 τρίτον ἦμαρ ἐυπλόκαμος τέλεσ' Ἠώς | 7.283-284 (Odysseus' account) ἐπὶ δ' ἀμβροσίη νὺξ ἤλυθ' |
| L+1 | 32 | −8 / −7 | Athena sends the dream to Nausicaa at night (6.13-47); the laundry; Odysseus slept "all night, into dawn and midday" and woke as the sun declined (7.288-289); "yesterday, on the twentieth day, I escaped the sea" (6.170); grove at sunset; palace (7.1-347); Alcinous promises the convoy for "tomorrow" (7.317-318). | 6.48 αὐτίκα δ' Ἠὼς ἦλθεν ἐύθρονος | 6.321 δύσετό τ' ἠέλιος; bed 7.344-347 |
| L+2 | 33 | −7 / −6 | Assembly, games, Demodocus (book 8); the tales of books 9-12 fill the night (11.330-332, 11.373 "this night is very long"; 11.350-351 "stay until tomorrow"); bed (13.17). | 8.1 ἦμος δ' ἠριγένεια… | 8.417 δύσετό τ' ἠέλιος; 13.17 |
| L+3 | 34 | −6 / −5 | Gifts to the ship, sacrifice, feast (13.18-28); Odysseus watches for sunset (13.29-35); embarks and sleeps (13.70-80); voyage overnight (13.81-92). | 13.18 | 13.33-35 κατέδυ φάος ἠελίοιο |
| **I** = L+4 | 35 | −5 / −4 | "When the brightest star rose, that comes to herald the light of early Dawn" the ship nears Ithaca (13.93-95); he is set ashore asleep, wakes (13.187); Athena; she leaves for Sparta (13.439-440); to Eumaeus (14.1); dinner (14.407); bed (14.523-533). | 13.93-95 (pre-dawn) | 14.457 νὺξ δ' ἄρ' ἐπῆλθε κακὴ σκοτομήνιος, rain all night (14.457-458) |

### 3.2 Telemachus' return and the two lines joining (books 15-23)

Athena finds Telemachus awake in Menelaus' porch "through the ambrosial night" (15.1-8). Pisistratus says "dawn will soon come" (15.50), and dawn comes "at once" (15.56). This night is the night of **I (sequential)** or the night of **I−1 (parallel)**.

| Day | dJ | B&M seq / par | Event [text] | Dawn | Nightfall |
|---|---|---|---|---|---|
| T1 | 36 | −4 / −4 | Telemachus leaves Sparta; Pherae (15.56-188). | 15.56 αὐτίκα δὲ χρυσόθρονος ἤλυθεν Ἠώς | 15.185-188 δύσετό τ' ἠέλιος…; night at Pherae |
| T2 | 37 | −3 / −3 | Pylos (15.193); Theoclymenus taken aboard (15.223-286); sails at sunset past Pheae and Elis (15.287-300). At the hut, "the two in turn" dine (15.301-302); Odysseus wants to go to town "at dawn" (15.308); Eumaeus' life story, "these nights are endless" (15.392); they sleep a little (15.493-494). | 15.189 | 15.296 δύσετό τ' ἠέλιος… |
| T3 | 38 | −2 / −2 | Telemachus lands at dawn (15.495-500) and goes to the hut (16.1-153); recognition; Eumaeus back in the evening (16.452); bed (16.481). The suitors' ambush ship comes home; they had kept watch every day and night (16.365-370). | 15.495 αἶψα γὰρ Ἠὼς ἦλθεν ἐΰθρονος; 16.2 ἅμ' ἠοῖ | 16.452 ἑσπέριος; 16.481 |
| T4 | 39 | −1 / −1 | To town; Argos; Antinous; Irus (17-18); "most of the day is gone" (17.190-191); late afternoon (17.606); Telemachus tells Eumaeus to come at dawn with victims (17.599-600); evening and braziers (18.306-307); Penelope sets the bow contest for tomorrow (19.571-581); Odysseus sleeps in the porch (20.1-55). | 17.1 | 18.306 μέλας ἐπὶ ἕσπερος ἦλθεν; 18.428 |
| **S** | 40 | 0 / 0 | **Festival.** Maids told the suitors will come early, "for it is a feast for all" (20.155-156); heralds lead the hecatomb through the city, the Achaeans gather in Apollo's grove (20.276-278); **Theoclymenus' vision during the meal (20.345-357)**, called a δεῖπνον before the coming δόρπον (20.390-394); "today is the holy feast of the god" (21.258-259); bow, slaughter (21-22); reunion (23). | 20.91 αὐτίκα δὲ χρυσόθρονος ἤλυθεν Ἠώς | 23.241-246 Athena holds back the dawn |
| S+1 | 41 | +1 | Laertes; the fighting; peace (23.347-24). | 23.347-348 | |

- **Hut nights.** Under the sequential reading Odysseus spends the nights of I, I+1, I+2 and I+3 at the hut. The day I+1 (dJ 36) and its night are **not narrated** for him. De Jong accepts this: book 15 covers "the last part of the night of the thirty-fifth day, the thirty-sixth and thirty-seventh day" [de Jong 2001, Book 15 summary].
- Under the parallel reading he spends three nights there (I, I+1, I+2), and 15.301-494 is his second evening.

### 3.3 Telemachus' outward days (for completeness; they do not change any offset)

| Day | Events and markers [text] |
|---|---|
| Day 1 | Council 1; Athena as Mentes. No dawn formula. Evening 1.423-424; Telemachus lies awake all night (1.443). |
| Day 2 | Dawn 2.1; assembly. Eurycleia's oath: say nothing for "the eleventh or twelfth day" (2.374). Sunset 2.388; sails all night until dawn (2.434). |
| Day 3 | Sunrise 3.1; Pylos. Sunset 3.329; bed 3.396-403. |
| Day 4 | Dawn 3.404; leaves Pylos. Sunset and Pherae 3.487-490. |
| Day 5 | Dawn 3.491. Sunset 3.497; arrives in Lacedaemon (4.1); bed 4.294-305. |
| Day 6 | Dawn 4.306. Menelaus asks him to stay "until the eleventh or twelfth day" (4.587-588); Telemachus says he cannot stay long (4.594-599). On Ithaca: Noemon saw Mentor here "yesterday at dawn" (4.655-656), so this scene is no earlier than Day 4 [me]. The suitors' plot (4.660-674). The ambush ship waits for evening (4.786) and sails to Asteris (4.842-847). Penelope's dream at night (4.795-841). |
| Day 7 = H | Dawn 5.1. Athena already knows of the plot (5.18-20). |

---

## 4. Every joint and its ambiguities

### A. Building the raft (5.228, 5.262-263): H→D = 5 (4)

- [text] Tools are given at the dawn of H+1 (5.228). Then: "it was the fourth day, and on it all was finished; on the fifth [day] Calypso sent him from the island" (5.262-263).
- **Mainstream (5).** Count the work days: H+1 is day 1, H+4 day 4, departure H+5. This is the reading of B&M, de Jong and Stanford.
- **Minority (4).** Count inclusively from Hermes' day, so H is day 1 and the departure is H+4. The Greek does not say what the ordinal counts from. But the work verifiably starts on H+1, and nothing in the text anchors the count to Hermes' day [me]. I know of **no** published chronology that uses 4. It is listed only as the far edge of what the wording allows.
- The formula itself shows Homer's ordinal style ("ninth... on the tenth", 7.253; "two days... the third", 5.388-390). The day the count starts from is day 1 [text; me].

### B. The departure and the 17 sailing days (5.263-279): D→Σ = 17 or 18

- [text] "Seventeen days he sailed... on the eighteenth the shadowy mountains appeared" (5.278-279). Odysseus repeats the count to Arete in the same words (7.267-268). The book 5 argument scholion says Poseidon saw him "on the eighteenth day" [schol. 1.5.1.1].
- **17.** He left in daylight on D, so D is sailing day 1 and Σ = D+17 (de Jong, Stanford).
- **18.** He left at or near sunset on D, so the 17 days start on D+1 and Σ = D+18 (B&M).
- The text gives no time of day for 5.263-269 [text]. Odyssean departures happen at every hour: Telemachus leaves Ithaca at night (2.388-434) and Pylos in the evening (15.296); the Phaeacians leave at sunset (13.33-80) [text]. **The text cannot settle this.** It is the only reason B&M's chain is one day longer than de Jong's.

### C. The drift (5.388-390) and the "twentieth day" (5.34, 6.170): Σ→L = 2

- [text] "There for two nights and two days he drifted... but when Dawn completed the third day" (5.388-390). On its own this allows the storm day to count as day 1 (landing Σ+2). It also allows the two days to follow the storm day (landing Σ+3).
- [text] Zeus forecasts that Odysseus will reach Scheria "on the twentieth day" (5.34). Odysseus tells Nausicaa, on L+1, "yesterday, on the twentieth day, I escaped the sea... from the island Ogygia" (6.170-172).
- The voyage begins on day 1 of the "seventeen" (§B), and the storm comes on day 18. So landing on day 20 means **L = Σ+2**, under either convention for D [me].
- The scholion on 6.170 reads it the same way. Naming only "the two days of the shipwreck" would move the girl less, so Odysseus gathers the whole number of days of his misfortune [schol. 1.6.2.171, H.P.Q.; paraphrase]. That is 17 + 1 + 2 = 20.
- Formulaic parallels (9.74-76, 10.142-144: two nights and two days, then the third day) fit the inclusive reading [text; me].
- **Σ+3 is defensible only if 6.170 is ignored.** I record it as an outer limit, not as a reading.
- Result: **D→L = 19** (17-day reading) **or 20** (18-day reading). B&M's "exactly 20 days and 20 nights at sea" is the 20 [B&M Table 1 note]. De Jong's numbers (Day 12 → Day 31) give 19 [me, from §6.2].

### D. Scheria: L→I = 4 (firm)

- [text] Dawns at 6.48 (L+1), 8.1 (L+2), 13.18 (L+3); the pre-dawn arrival at 13.93-95 (L+4).
- Odysseus slept from the evening of L (7.283-284) to the afternoon of L+1 (7.288-289). Aristarchus' reading δείλετο, and the scholion on it, put the meeting with Nausicaa before sunset on that day [schol. 1.7.2.265-266].
- The tales of books 9-12 take one night (11.373; 13.17).
- No reading changes this.

### E. The overnight voyage and the morning star (13.70-95): Venus is on I, before dawn

- [text] He boards after sunset on L+3 (13.33-35, 13.70-80). "When the brightest star rose, the one that most of all comes heralding the light of early-born Dawn, then the ship drew near the island" (13.93-95).
- The scholion glosses ὑπερέσχε as "until it rose above" [schol. 2.13.2.64, Q].
- Reading the star as Venus (a morning star) is B&M's and standard [B&M]. The text says only that it is the brightest star and heralds dawn.
- **Day labelling.** The sighting is in the pre-dawn of I. By civil day it is I (B&M −5 seq). By the night it belongs to, it is the night of L+3 (−6 seq) [me]. This is one possible source of the press release's "six" (§2.3).

### F. Athena's night in Sparta and the hut: I→S = 5 or 4

- [text] Athena leaves Odysseus for Sparta at 13.439-440. Book 15 opens with her arriving and finding Telemachus awake at night (15.1-8). Dawn follows at once (15.56). Then three dawns at 15.56, 15.189 and 15.495 lead to the landing on Ithaca, and two more at 17.1 and 20.91 lead to the festival.
- The scholion on 15.1 says Athena's going is "not now, but when Odysseus recognized his homeland", that is, at 13.439 [schol. 2.15.4.1, Q]. Ancient readers took 15.1 as picking up 13.440 rather than as a new departure. It does not say on which night she arrived.
- **Sequential: 5** (de Jong, Apthorp, Delebecque, Hellwig, B&M seq).
  - She arrives on the night of I, after the scene on the shore.
  - Telemachus' T1 = I+1 and S = I+5.
  - Cost: Odysseus' day I+1 at the hut is never narrated.
- **Parallel: 4** (B&M par; Stanford as tabulated).
  - She reaches Sparta before dawn on I, so T1 = I and S = I+4.
  - Gain: 15.301-494 becomes Odysseus' second evening, with no silent day.
  - Cost: all of 13.187-440 has to happen before dawn on I. That includes Odysseus waking, the long talk, and Athena scattering the mist so he can see the harbour, the olive, the cave and Neriton (13.344-352). The ship only arrived when the morning star rose. B&M require Venus to rise at least 90 minutes ahead of the Sun, and for 1178 they compute 1 h 43 min [B&M *Intersecting*].
- **6** would need Athena to arrive only on the night of I+1, a full day after leaving Ithaca, with two silent days for Odysseus. Nothing in the text suggests a delay. **Not defensible** [me].

### G. Ithaca, from Telemachus' landing to the festival (firm)

- [text] Dawns at 15.495 / 16.2, 17.1 and 20.91, and a nightfall at 18.306. T3 and T4 are single days (de Jong: book 17 "starts day thirty-nine, which will end in 20.90").
- No reading changes this.

### H. Which day Theoclymenus speaks: S

- [text] On the day that begins at 20.91. It is the festival day: 20.155-156, 20.276-278, and 21.258-259, where 21.267 names Apollo.
- He speaks while the suitors are eating, "a meal (δεῖπνον)... but no supper (δόρπον)" uglier than the one about to come (20.390-394). The slaughter follows the same day (21-22).
- No clock time is given. The suitors arrived "very early" (20.156). Homeric δεῖπνον is the main meal and can fall early (16.2 calls breakfast ἄριστον). B&M's "noontime meal" is an inference that fits the eclipse's computed 12:02 [B&M Fig. 1].
- The scholia deny an eclipse took place: there was no eclipse; Theoclymenus sees it in prophetic frenzy, "that the sun will be eclipsed for them" [schol. 2.20.2.91, B; V].

### I. Which nights the Pleiades and Boötes are watched (5.270-277)

- [text] The verbs are imperfect and the participle present (ἰθύνετο, ἔπιπτεν, ἐσορῶντι), followed by the summary "seventeen days he sailed" (5.278). This is **habitual action over the whole voyage**, not one night [me].
- B&M themselves say he "navigates by these stars every night until sunk" and require the whole voyage to fall in the visibility window [B&M *References*]. Their headline constraint is the **first** night.
- Number of nights before Σ [me]:
  - 17 (de Jong): the evenings of D through D+16.
  - 18 (B&M): the evenings of D through D+17.
- Offsets: evenings from S−29 to S−12 (B&M seq), S−28 to S−11 (par), S−28 to S−12 (de Jong), S−27 to S−11 (Stanford). The union is **S−29 to S−11**.
- 5.273-275 repeat Iliad 18.487-489 word for word, the stars on Achilles' shield [text; `iliad-grc.tsv`]. A P-scholion notes the same [schol. 1.5.2.252]. Friedländer's Aristonicus prints it as an Aristarchan ὅτι-note, at 5.273-275 in `data/text/aristonicus-signs-odyssey-grc.tsv`.
- The "late-setting" Boötes was explained in antiquity through Aratus: it sets slowly, across four zodiac signs [schol. 1.5.2.244].

### J. Telemachus' timeline and the Spartan inconsistency

- [text] Telemachus says he cannot stay (4.594-599). Menelaus suggests 11 or 12 days (4.587-588). Eurycleia's oath is to keep silent until the 11th or 12th day (2.374, 4.747-748). Yet he is still in Sparta when Athena comes (15.1-10: "it is no longer right to wander far from home").
- Apthorp counts from Day 6 (4.624) to the pre-dawn of Day 36 (15.1), and argues the poet meant a long stay [Apthorp 1980, CQ 30.1, p. 1, first-page extract; he cites Delebecque 1958 facing p. 12 and Hellwig 1964 pp. 42-44 for the day plan]. Page 1955 (pp. 66-67, 77-79) treated it as a fault of composition [as cited by Apthorp].
- De Jong: by "continuity of time" the same 29 days pass for Telemachus as for Odysseus [de Jong 2001, Book 15 summary].
- The suitors' ambush ship waits from the evening of Day 6 until T3 (4.786, 4.842-847, 16.365-370).
- **Effect on the offsets:** none, except through joint F. The Telemachy runs parallel to H through I and gives no independent link to Odysseus' days.
  - B&M's parallel column also puts council 1 on the same day as council 2 (−33). Athena's knowledge of the plot at 5.18-20 sits awkwardly with that [me]. It does not affect H→S.

### K. Ambiguities that change what Day 0 *is*, not how far away it is (brief; for the lunar and festival tests)

- **"As this month wanes and the next begins"** (14.162 = 19.307). The scholia gloss it as "the thirtieth and the new moon... that is, the old-and-new day" [schol. 2.14.2.94, Q.V.]. Heraclitus ties it to eclipses on the "thirtieth and new-moon day" [Heraclitus, *Homeric Problems*: chapter numbered LXXIII in library edition 3322, §75 in B&M's citation]. Plutarch's speaker pairs 20.351-357 with the same line [*De facie* 19, Cherniss tr.].
  - But Hesiod uses φθίνοντος and ἱσταμένου as the waning and waxing *parts* of the month for counting days (*Works and Days* 798). So the phrase can also be read as a window, not a single day [me; text of WD in library edition 728].
  - 14.162-164 were suspected in antiquity as out of step with the lines before them and implausible ("how could he know…?"). The scholion is in manuscript H, and manuscript M marks the lines with obeli. Both are collected in Friedländer's Aristonicus at 14.162-164, in the file `aristonicus-signs-odyssey-grc.tsv`.
- **λυκάβας** (14.161, 19.306). The scholia gloss it as "year" [schol. 2.14.2.93, 2.19.2.115]. Murray translates "day" at 14.161 and "month" at 19.306 [Murray].
- **σκοτομήνιος** (14.457). The scholia give "moonless, dark; or [the night] in which the moon is darkened by its conjunction with the sun" [schol. 2.14.2.238, V; P]. Taken literally as the conjunction, it puts conjunction about 4-5 days *before* S, which conflicts with an eclipse on S [me].
- **Whose festival, and which day.** The festival is Apollo's (20.276-278, 21.267). The scholia say the new-moon day was sacred to Apollo, who was called Neomenios, citing Philochorus [schol. 2.20.2.42, V]. Another scholion has the poet set the slaughter on a festival so that the men are busy [schol. 2.20.2.43, V]. But Hesiod makes the **seventh** the holy day on which Leto bore Apollo (*Works and Days* 770-771). The text never says the festival falls on the new moon [me].
- **Ancient eclipse readings.** An ancient papyrus commentary reportedly cites Aristonicus and Aristarchus of Samos on the new moon and eclipses here (P.Oxy. 53.3710). I know it only from a blog translation (sententiaeantiquae.com, 2017), so it is **secondary**.

---

## 5. Interval table

Each row gives S − X in days unless the row says otherwise. Readings: H→D is 5 (or 4 inclusive); D→L is 19 (D counted as day 1) or 20 (sunset departure); L→I is always 4; I→S is 5 (sequential) or 4 (parallel).

| Interval | B&M paper (seq) | B&M par | Min | Max | Reading at min | Reading at max |
|---|---|---|---|---|---|---|
| **H → S (Hermes, Mercury)** | **34** | 33 | **32** (31) | **34** | 5 + 19 + 4 + 4. The 31 adds the inclusive raft count (4). | 5 + 20 + 4 + 5 |
| H → D (raft) | 5 | 5 | 4 | 5 | inclusive from H | work days from H+1 |
| **D → S (first raft night, Pleiades/Boötes)** | **29** | 28 | **27** | **29** | 19 + 4 + 4 | 20 + 4 + 5 |
| Any raft night → S | 29..12 | 28..11 | **11** | **29** | last night before Σ, I→S = 4 | first night, max chain |
| D → Σ | 18 | 18 | 17 | 18 | D is sailing day 1 | sunset departure |
| Σ → L | 2 | 2 | 2 | 2 (3 if 6.170 is ignored) | 6.170 + 5.34 | — |
| D → L | 20 | 20 | 19 | 20 | as for D → Σ | as for D → Σ |
| L → I | 4 | 4 | 4 | 4 | firm | firm |
| **I → S (Venus)** | **5** | 4 | **4** | **5** | parallel Sparta night | sequential |
| Σ → S (Poseidon, equinox) | 11 | 10 | 10 | 11 (12) | | |
| L → S | 9 | 8 | 8 | 9 | | |
| H → I (Mercury → Venus) | 29 | 29 | 28 (27) | 29 | | |
| D → I (first Pleiades night → Venus) | 24 | 24 | 23 | 24 | | |
| Night of 14.457 → S | "−2" (B&M's text; their own table says −5) | | night of S−4 | night of S−5 | | |
| Theoclymenus → slaughter | 0 | 0 | 0 | 0 | same day (20.91 → 22) | |

### 5.1 The full reading grid, for the null-model agent

```tsv
build_HtoD	sea_DtoL	ithaca_ItoS	Mercury_H	PleiadesFirst_D	PleiadesLast	Storm_Sigma	Landing_L	Venus_I	note
5	20	5	34	29	12	11	9	5	B&M sequential (paper's search)
5	20	4	33	28	11	10	8	4	B&M parallel
5	19	5	33	28	12	11	9	5	de Jong 2001 / Apthorp / Delebecque (41 days)
5	19	4	32	27	11	10	8	4	Stanford 1959 as tabulated by Struck (40 days)
4	20	5	33	29	12	11	9	5	inclusive raft count (no published chronology)
4	20	4	32	28	11	10	8	4	inclusive raft count
4	19	5	32	28	12	11	9	5	inclusive raft count
4	19	4	31	27	11	10	8	4	inclusive raft count
```

All values are days before S. "PleiadesLast" is the evening date of the last raft night before the storm. Offsets of Σ, L and I do not depend on the raft count.

- Eight readings, plus a free choice of night for the Pleiades. B&M's chosen reading is the corner (34, 29, 5).
- **Fair test.** A null model should either treat the reading as a nuisance parameter or apply the same "take the reading that fits" freedom to every candidate date. B&M say only the sequential fit is "exact".
- **Press-release triple.** (33, 29, 5) does occur in the grid, from the inclusive raft count plus the sunset departure. (33, 29, 6) does not occur under any reading.

---

## 6. Scholarly chronologies

### 6.1 Ancient

- **Scholia (Dindorf; read directly):**
  - Argument to book 5: Poseidon sees him "on the eighteenth day" [1.5.1.1, P.Q.V.].
  - Alternative argument to book 8: **"Day 23, on which the Phaeacians hold an assembly about the stranger…"** [1.8.2.1, H.P.Q.]. This is the only numbered day in the collection. The argument to book 1 ("on the day in which there is an assembly of the gods", Ἡμέρᾳ ἐν ᾗ, Q) and to book 2 ("at dawn", H.M.S.) look like remnants of the same day-by-day scheme [me].
    - The anchor is not stated. Counting from the departure as day 1, the assembly is L+2, so the departure is Day 1 and the landing Day 21, which needs D→L = 20. That is B&M's interval, with de Jong's 19 giving Day 22 [me].
    - Counting from the day the raft was finished would give 23 with D→L = 19.
    - No anchor in the Telemachy or on Hermes' day can give 23 [me].
  - Scholion on 6.170 (§4.C), on 15.1 (§4.F), on 14.162, 14.457, 20.155 and 20.356 (§4.H, §4.K).
- **Aristonicus (Aristarchan signs, Friedländer's collection; library edition 3257, read directly):**
  - 14.162-164 suspected (scholion in H; obeli in M);
  - a note at 5.273-275 on the Iliad repeat;
  - a diple at 5.277 noting that he sails from the Atlantic region eastward.
- **Heraclitus, *Homeric Problems*** (library edition 3322): reads 20.351-357 as an eclipse, places eclipses on the "thirtieth and new-moon day", and quotes 14.162.
- **Plutarch, *De facie* 19** (library editions 369 and 371): pairs Theoclymenus' words with "when waning month to waxing month gives way" (14.162 / 19.307).
- None of these ancient sources gives a full 40-day count. Apart from the "Day 23" notice, they bear only on single joints.

### 6.2 Modern

| Source | How read | H | D | Σ | L | I | T1 | S | Total |
|---|---|---|---|---|---|---|---|---|---|
| de Jong, *A Narratological Commentary on the Odyssey* (CUP 2001), Appendix A | **Secondary within the book**: CUP's chapter summaries, not Appendix A itself. Book 5 = days 7 to the first part of 32; book 7 = evening of 32; book 8 = day 33 until 13.17; book 13 = days 34 and part of 35; book 14 = rest of 35; book 15 = end of the night of 35, days 36-37, early 38; book 16 = 38; book 17 starts 39, ending at 20.90; book 23 = end of 40 and start of 41. D and Σ are my inference. | 7 | 12 | 29 | 31 | 35 | 36 | 40 | 41 |
| Apthorp 1980, CQ 30.1, 1-22 (after Delebecque 1958; Hellwig 1964) | First-page extract only: Telemachus is left on Day 6 and taken up again in the pre-dawn of Day 36. | 7? | | | | 35 | 36 | 40? | 41? |
| Monro 1901 (*Odyssey* XIII-XXIV commentary) | **Secondary**, quoted by "The Homer Reader": 13.18 = "morning of the 34th day"; 13.93 = "the dawn of the 35th day". The Homer Reader's own table is internally inconsistent, so not used. | | | | | 35 | | | |
| Stanford 1959 (*Odyssey* commentary, pp. xx-xxii) | **Secondary**, tabulated by P. T. Struck (UPenn "Forty Day Chronology"). Days 8-11 raft; 12-28 sailing; 29 storm; 30-31 to Scheria; 32 Nausicaa; 33 books 8-13; 34 "drop off at Ithaca"; 35-36 at Eumaeus' while Telemachus goes Pherae-Pylos-home; 37 Telemachus arrives; 39 slaughter. The table runs the gifts day into the arrival; Telemachus reaching the hut on Day 37 implies T1 = I = 35, i.e. parallel. | 7 | 12 | 29 | 31 | 35 | 35 | 39 | 40 |
| B&M 2008, sequential | read | −34 (Day 7) | −29 (12) | −11 (30) | −9 (32) | −5 (36) | −4 (37) | 0 (41) | 42 |
| Papamarinopoulos et al. 2012, MAA 12(1) 117-128 | **Secondary** (search snippet): return to Ithaca 5 days before an annular eclipse on 30 October 1207 BC. | | | | | S−5 | | | |

- **Not read:**
  - Gainsford 2012, the classicist's reply to B&M (TAPA 142.1, 1-22): Project MUSE served a CAPTCHA, which I did not try to get around.
  - Schoch 1926: a sibling agent saved it at `data/bm2008-a/schoch-1926-observatory-49-19.pdf`. I did not read it for chronology.
  - MacDonald 1967, JBAA 77, 324-328 ("The season of the Odyssey").
  - Hoekstra's and Russo's volumes of the Oxford commentary.
  - Hölscher 1939; Delebecque 1958 and Hellwig 1964 directly.

---

## 7. Consequences for the bench

1. **Use ranges, not single values.**
   - Mercury: H = S−31..34. The core range is 32-34; 31 only under the inclusive raft count.
   - Pleiades and Boötes: the first night S−27..29, and every voyage night S−11..29.
   - Venus: S−4..5.
   - Poseidon and the equinox: S−10..11.
   - The moonless night of 14.457: the night of S−5 or S−4, not S−2.
2. **B&M's sequential reading is the maximal corner of the grid.** It rests on a sunset departure the text does not state. It is one day longer than the standard commentary (de Jong) on the Ogygia side and agrees with it on Σ, L and I.
3. **The Ithaca joint (I→S = 4 or 5) can be argued either way.** The sequential reading is the scholarly default (de Jong, Apthorp). The parallel reading has economy of narration on its side but strains the pre-dawn timeline.
4. **Positive-control design.** Any control text should be put through the same grid. The test is whether the claimed date survives across readings, or only in the one reading that was chosen after looking at the sky.

---

## 8. Open questions and gaps

- Departure time from Ogygia (morning or sunset) cannot be decided from the text. It is the 19-versus-20-day hinge.
- The night of Athena's arrival in Sparta (the night of I−1 or of I) is the 4-versus-5-day hinge. Hoekstra's commentary on 15.1-56 should be checked.
- The anchor of the scholiast's "Day 23" (book 8 argument) is unknown. Are there similar numbered notices in manuscripts H, P or Q that Dindorf did not print?
- Not read directly: de Jong's Appendix A (only CUP chapter summaries); Stanford's own table (only Struck's version); Monro (only as quoted); Gainsford 2012 (CAPTCHA); MacDonald 1967; Papamarinopoulos 2012 (only a search snippet); P.Oxy. 3710 (only a blog translation).
- B&M's internal inconsistencies to put to the reproduction agent:
  - Hermes on 13 March (main text) or 15 March (SI Table S1).
  - "Night −2" for 14.457.
  - Pleiades last visibility on 3 or 4 April.
  - New moon or "full moon" at departure.
- B&M's "local time" convention (mean or apparent) is not stated.
- Day 0's identity:
  - the turn-of-month day, or a waning-and-waxing window (14.162; Hesiod *Works and Days* 798);
  - Apollo's festival on the new moon (Philochorus, cited in the scholia) or on the seventh (*Works and Days* 770-771);
  - σκοτομήνιος as moonless, or as the night of conjunction.

## Sources consulted

- Greek text and translations: `data/text/odyssey-grc.tsv`, `odyssey-murray.tsv`, `odyssey-butler.tsv`, `iliad-grc.tsv` (18.483-489).
- Scholia and ancient readers: `data/text/scholia-odyssey-grc.tsv`; ClassicaCodex exports (read-only, via `odybench.ccx`): `aristonicus-signs-odyssey-grc.tsv` (edition 3257), `heraclitus-allegoriae-grc.tsv` (3322), `plutarch-de-facie-grc.tsv` (371), `plutarch-de-facie-cherniss.tsv` (369); Hesiod *Works and Days* (edition 728, read through `odybench.ccx.nodes`).
- B&M 2008, full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC2440358/ (DOI 10.1073/pnas.0803317105). SI text layer: `data/bm2008-a/baikouzis-magnasco-2008-SI.pdf`.
- Press release: https://www.rockefeller.edu/news/2305-celestial-clues-hint-at-eclipse-in-homers-odyssey/ and https://www.eurekalert.org/news-releases/749744
- de Jong 2001 chapter summaries: https://www.cambridge.org/core/books/abs/narratological-commentary-on-the-odyssey/book-fifteen/580EB3CC71DBF742D45084F9133FFDB5 and the sibling pages for books 4, 5, 7, 8, 13, 14, 16, 17 and 23.
- Apthorp 1980: https://www.cambridge.org/core/journals/classical-quarterly/article/abs/obstacles-to-telemachus-return/77370E2A68FD1699291E7E71BB083584
- Stanford's table via Struck: https://www2.classics.upenn.edu/myth/php/homer/index.php?page=dayline
- Monro as quoted: https://johnhboyer-sys.github.io/homer-reader/timeline/
- P.Oxy. 3710, secondary: https://sententiaeantiquae.com/2017/08/20/an-eclipse-in-the-odyssey/
- Gainsford 2012, not read: https://muse.jhu.edu/article/476076
