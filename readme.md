
Twitter #trend Recommendation using Topic Models
================================================





Entities
--------

Tweet obj:
 * user_id: ID of the user who tweeted, as per twitter
 * text: content
 * id_str: ID of this tweet, as per twitter
 * lang: ISO Language Code, only 'en' right now
 * coord: (lat, long) of tweet's location, as per twitter
 * loc: of user, as per twitter
 * created_at: time of creation, as per twitter
 * trend_ids[ ]: a list of unique internal trend IDs being recorded where we saw this tweet
 * retweeted: YES/NO
 * retweet_id: ID of the tweet this tweet is a retweet of

User obj:
* id_str: ID of the user who tweeted, as per twitter
* location: location sepcified by this twitter account
* name: Name of the user on this twitter account
* screen_name: @handle of this twitter account
* trend_ids [ ]: A list of unique internal trend IDs being recorded, this user tweeted about
* tweets[ ]: A list of all tweets we have seen that belong to this user

Trend Obj:
* trend: name of trend
* trendid: unique number, auto-incr


Roadmap
-------
* Represent a #trend accurately with an [LDA](http://machinelearning.wustl.edu/mlpapers/paper_files/BleiNJ03.pdf) topic model with [Gensim](https://github.com/piskvorky/gensim).

* Gensim still doesn't implement a purely online version of LDA, or of a Dynamic Topic Model which are the perfect model to represent a corpus which is temporally evolving in topics - thus suiting a twitter trending topic closely.
 * Neither could I come across a mature and maintained implementation of Dynamic Topic Models in Python at all.
 * Hence, as a prototype the current aim is to model a static corpus accurately and implement a bare-bones recommendation system with it, i.e. give a #trend, it could recommend you other trends on twitter at that given moment which are topically similar to this trend, or in other words, recommend other trends with similar topic distributions to the given trend.

* Ultimately,
 * Automate tweet collection and learning of the topic model online, perhaps this would enforce a migration to C++ or working something out with Gensim in the future
 * Make this recommendation system live! Probably exposed as a webapp.


RESULTS THUS FAR
================

Online LDA:
-----------


### **ONLINE LDA (50 TOPICS):** _Topics start to disperse with infrequent words_

topic #49 (0.020): diegogarcia, lead, finding, officials, message, wood, rush, phillip, huge, philip

topic #48 (0.020): live, perth, base, raaf, pearce, visit, centre, man, space, heading

topic #47 (0.020): indonesian, minister, abbott, hq, prime, steered, ended, ht, global, statement

topic #46 (0.020): australia, avoid, auspol, trips, telegraph, nations, place, landing, cautions, bahrain

topic #45 (0.020): passengers, probe, teams, crews, board, great, work, continues, hears, analysis

topic #44 (0.020): aviation, guy, track, deployed, allah, solved, located, listening, bring, google

topic #43 (0.020): anwar, leader, opposition, life, chance, isn, noise, buried, fighter, food

topic #42 (0.020): find, wing, stop, real, grief, helped, abt, hagel, chuck, clear

topic #41 (0.020): ships, area, today, aircraft, consistent, involved, boeing, km, operation, fully

topic #40 (0.020): days, important, battery, revelation, mcdonald, left, reporting, facts, airasia, kerguelen

topic #39 (0.020): ping, data, acoustic, hours, frequency, information, secret, theory, investigate, mas

topic #38 (0.020): flying, set, discussing, curious, run, case, investigated, safe, missed, quick

topic #37 (0.020): australian, houston, day, race, official, angus, weeks, disappeared, investigating, agency

topic #36 (0.020): deep, site, home, cargo, crew, flown, lot, clue, coming, special

topic #35 (0.020): black, box, ship, signals, pulse, pinger, underwater, shield, hms, navy

topic #34 (0.020): chinese, families, story, happened, big, proof, answers, tech, top, wt20

topic #33 (0.020): good, government, calls, recorder, running, sunday, transcript, night, told, malaysian

topic #32 (0.020): confirm, thought, pinging, sense, xinhua, wow, helping, saracens, ulster, sick

topic #31 (0.020): pings, reports, vessel, false, detect, hour, event, guess, equipment, powerball

topic #30 (0.020): searchers, hoping, ds, hishammuddin, lingering, reason, onset, miller, mind, lie

topic #29 (0.020): indonesia, sar, high, mission, sian, contact, records, verified, fire, hey

topic #28 (0.020): pray, god, meeting, jim, clancy, director, poses, bless, mark, fades

topic #27 (0.020): don, conspiracy, theories, north, doesn, miles, understand, concealing, job, role

topic #26 (0.020): boxes, joins, info, underwater, water, aliens, cia, holes, sound, hijacked

topic #25 (0.020): disappearance, truth, read, pilots, relatives, updates, practice, guys, gov, step

topic #24 (0.020): latest, president, datuk, campaign, authorities, safety, speculation, hopeful, events, nst

topic #23 (0.020): jacc, chief, investigation, winning, police, wife, defence, arrives, shows, related

topic #22 (0.020): debris, southern, source, tweet, continue, team, sharing, newspaper, berita, harian

topic #21 (0.020): locate, full, international, reach, suspected, bottom, oceanshield, agree, damn, malaysianairlines

topic #20 (0.020): diego, difficult, garcia, electronic, south, revealed, means, article, experts, land

topic #19 (0.020): conference, coverage, leads, promising, history, najib, wait, due, move, week

topic #18 (0.020): malaysiaairlines, radar, world, turn, separate, landed, inmarsat, tells, countries, victims

topic #17 (0.020): picks, verify, wreckage, map, floor, cleared, locators, claim, palace, supposed

topic #16 (0.020): surface, island, moon, morning, encouraging, praying, fact, kerguelen, recording, working

topic #15 (0.020): alive, goharshahi, younusalgohar, april, disclosed, uk, cockpit, showing, 1st, covering

topic #14 (0.020): detected, echo, crash, satellite, usa, hijacking, floating, diegogarcia, images, pressure

topic #13 (0.020): air, military, tracking, jets, force, arrived, unidentified, royal, freescale, join

topic #12 (0.020): heard, close, investigators, vanished, finally, path, put, route, dead, control

topic #11 (0.020): tragedy, family, reported, russia, govt, shadows, country, drama, criminal, love

topic #10 (0.020): news, breaking, head, british, interesting, intense, stay, sky, report, wtf

topic #9 (0.020): china, painstaking, rest, sad, call, cracked, peace, fb, pages, death

topic #8 (0.020): sounds, human, confirmed, cover, prayers, watching, science, thoughts, positives, bbc

topic #7 (0.020): ocean, indian, evidence, pulses, whales, crashed, hard, depth, intact, happen

topic #6 (0.020): malaysian, month, lost, sea, location, flew, true, batteries, update, airline

topic #5 (0.020): blackbox, passenger, video, diegogarcia, give, falseflag, online, humankind, 2nd, talking

topic #4 (0.020): signal, airlines, hunt, detects, searching, spotted, haixun, intensifies, objects, zone

topic #3 (0.020): time, watch, mystery, media, people, long, begins, intelligence, post, hearing

topic #2 (0.020): cnn, press, haven, runs, briefing, fuel, deadline, talk, haystack, needle

topic #1 (0.020): hope, planes, airspace, patrol, hear, confirmation, waiting, lose, hamper, malaysiancrash

topic #0 (0.020): smear, slams, questions, pilot, picked, claims, baseless, peter, making, breakthrough







### **ONLINE LDA (40 TOPICS):** _Topics begin to look incomplete_

topic #39 (0.025): diegogarcia, passenger, falseflag, revealed, confirmed, cnn, finally, photo, quest, criminal

topic #38 (0.025): australian, live, watch, perth, hours, vessel, base, theory, batteries, details

topic #37 (0.025): planes, diego, garcia, electronic, south, hard, land, hamper, maldives, arrives

topic #36 (0.025): searching, story, picks, deep, reporting, wreckage, big, map, experts, floor

topic #35 (0.025): pings, reports, avoid, joins, false, home, event, hq, nations, clue

topic #34 (0.025): hunt, don, blackbox, video, online, intense, concealing, won, blog, role

topic #33 (0.025): race, secret, question, guy, allah, solved, listening, intelligence, nuclear, practice

topic #32 (0.025): anwar, conspiracy, pilot, theories, revelation, govt, track, rest, cockpit, humankind

topic #31 (0.025): disappearance, truth, hell, shot, buried, wow, guys, gov, miller, key

topic #30 (0.025): days, authorities, mcdonald, police, wife, cover, aboard, frustrated, oceanshield, statement

topic #29 (0.025): people, military, lost, sea, north, tracking, hoping, miles, possibly, saturday

topic #28 (0.025): houston, smear, slams, angus, questions, chief, verify, agency, marshal, knew

topic #27 (0.025): frequency, crash, satellite, close, flying, tech, images, jim, vessels, years

topic #26 (0.025): find, debris, technology, winning, crews, isn, team, april, shows, mh370qs

topic #25 (0.025): signal, ocean, indian, detects, consistent, evidence, patrol, pulses, whales, crashed

topic #24 (0.025): turn, abbott, auspol, great, continues, flown, special, skirted, verified, tony

topic #23 (0.025): finding, important, sounds, press, probe, locate, facts, doesn, airasia, clues

topic #22 (0.025): ping, china, leader, opposition, world, minister, source, british, najib, closure

topic #21 (0.025): diegogarcia, day, sar, investigation, real, message, mission, article, running, phillip

topic #20 (0.025): island, location, conference, airspace, claims, chance, begins, boeing, confirmation, waiting

topic #19 (0.025): datuk, campaign, hear, full, xinhua, oceans, thinking, problem, missingplane, brings

topic #18 (0.025): news, breaking, malaysiaairlines, echo, cnn, true, speculation, aliens, moon, confirm

topic #17 (0.025): safety, information, separate, thought, country, dont, love, tv, helped, system

topic #16 (0.025): month, radar, good, tragedy, flew, teams, russia, mas, fly, painstaking

topic #15 (0.025): detected, usa, hijacking, sian, vanished, wait, lies, director, path, transcript

topic #14 (0.025): malaysian, cnn, time, lead, officials, coverage, long, cargo, contact, hold

topic #13 (0.025): air, official, investigators, force, arrived, briefing, uk, steered, analysis, royal

topic #12 (0.025): passengers, wing, family, morning, board, praying, families, shadows, airline, crew

topic #11 (0.025): data, searchers, jacc, leads, head, tweet, promising, detect, defence, sharing

topic #10 (0.025): surface, history, jets, hears, journey, move, week, fact, biggest, increases

topic #9 (0.025): black, box, ship, signals, pulse, underwater, mystery, pinger, shield, area

topic #8 (0.025): southern, investigate, continue, encouraging, leave, sec, poses, caught, mcdonald, space

topic #7 (0.025): black, boxes, acoustic, battery, water, left, read, high, sound, runs

topic #6 (0.025): chinese, families, latest, president, stop, pray, government, indonesian, god, meeting

topic #5 (0.025): ships, today, area, aircraft, happened, difficult, involved, cia, hijacked, simulator

topic #4 (0.025): life, weeks, update, disappeared, proof, show, baseless, recorders, impossible, secrets

topic #3 (0.025): heard, indonesia, alive, goharshahi, younusalgohar, pilots, human, check, means, pressure

topic #2 (0.025): spotted, picked, info, work, floating, objects, zone, kerguelen, suspicious, white

topic #1 (0.025): airlines, australia, aviation, intensifies, nst, centre, man, dead, showing, bring

topic #0 (0.025): hope, media, give, reported, trips, top, wt20, related, drama, state







### **ONLINE LDA (35 TOPICS):** _A cohesive unit --OPTIMUM_

topic #34 (0.029): live, watch, don, indonesia, happened, cnn, north, batteries, proof, pingers

topic #33 (0.029): reports, sounds, jacc, island, head, human, tweet, revealed, interesting, defence

topic #32 (0.029): australia, day, crash, long, speculation, hopeful, set, telegraph, watching, vessels

topic #31 (0.029): people, latest, lost, encouraging, tells, centre, man, fact, times, lt

topic #30 (0.029): picks, leads, aliens, moon, promising, big, question, trips, home, hoping

topic #29 (0.029): china, black, boxes, days, battery, water, left, usa, high, hijacking

topic #28 (0.029): official, verify, wt20, briefing, helped, poses, channel, kl, revolutionary, kalkiavatar

topic #27 (0.029): alive, goharshahi, younusalgohar, floating, disclosed, running, state, potential, pretty, food

topic #26 (0.029): families, finding, life, press, info, conference, chance, hear, begins, chinese

topic #25 (0.029): wing, passenger, cover, investigators, arrives, secrets, xinhua, bbc, tonight, sec

topic #24 (0.029): race, consistent, probe, secret, theory, aviation, confirm, turn, cargo, details

topic #23 (0.029): sar, avoid, work, mission, airline, nations, analysis, biggest, survivors, bahrain

topic #22 (0.029): australian, ships, area, today, perth, searching, spotted, haixun, base, involved

topic #21 (0.029): ocean, detected, indian, searchers, stop, planes, false, pulses, whales, depth

topic #20 (0.029): diego, garcia, electronic, ll, russia, mt, land, km, send, dont

topic #19 (0.029): world, military, picked, crashed, april, runs, cockpit, uk, deployed, lol

topic #18 (0.029): time, air, patrol, minister, investigation, source, investigate, isn, jets, najib

topic #17 (0.029): find, data, sea, deep, authorities, teams, real, close, wreckage, police

topic #16 (0.029): box, black, ship, signals, pulse, underwater, pinger, shield, evidence, hms

topic #15 (0.029): vessel, indonesian, mcdonald, british, events, mas, kerguelen, hell, shot, international

topic #14 (0.029): houston, malaysiaairlines, important, disappearance, angus, echo, blackbox, chief, claims, flew

topic #13 (0.029): passengers, datuk, true, meeting, wife, tech, crew, arrived, event, sunday

topic #12 (0.029): campaign, pilots, recorder, aboard, hearing, investigated, indianocean, vigorous, titanic, saracens

topic #11 (0.029): signal, pings, news, breaking, cnn, detects, difficult, coverage, read, experts

topic #10 (0.029): diegogarcia, hope, give, locate, falseflag, message, waiting, wood, maldives, talking

topic #9 (0.029): location, southern, winning, south, continue, govt, vanished, inmarsat, finally, nst

topic #8 (0.029): ping, acoustic, good, weeks, pray, god, frequency, site, disappeared, wait

topic #7 (0.029): smear, slams, questions, conspiracy, pilot, theories, debris, revelation, safety, online

topic #6 (0.029): lead, radar, aircraft, hours, joins, airspace, satellite, board, boeing, doesn

topic #5 (0.029): mystery, media, story, morning, praying, thought, shadows, landed, jim, related

topic #4 (0.029): airlines, heard, anwar, leader, opposition, officials, tragedy, reporting, sian, mh370qs

topic #3 (0.029): malaysian, month, update, show, multiple, words, movie, hey, seconds, twin

topic #2 (0.029): president, government, flying, confirmed, calls, discussing, director, countries, stay, increases

topic #1 (0.029): hunt, surface, video, technology, reported, team, check, hamper, shows, updates

topic #0 (0.029): chinese, family, discovers, relatives, painstaking, answers, rest, beijing, fly, sad







### **ONLINE LDA (25 TOPICS):** _Looks almost good_

topic #24 (0.040): race, diegogarcia, consistent, sounds, probe, patrol, chance, hear, aviation, falseflag

topic #23 (0.040): boxes, radar, air, jacc, chief, water, govt, boeing, fly, defence

topic #22 (0.040): lead, indonesian, airspace, claims, false, verify, tracking, landed, painstaking, haven

topic #21 (0.040): anwar, leader, surface, opposition, reports, conference, head, source, begins, tweet

topic #20 (0.040): perth, indonesia, stop, info, military, winning, real, base, full, intensifies

topic #19 (0.040): latest, campaign, story, avoid, long, pilots, jets, means, set, arrived

topic #18 (0.040): signal, ocean, indian, detects, searchers, island, southern, north, pulses, crews

topic #17 (0.040): heard, locate, team, hell, xinhua, cleared, buried, reach, sec, bottom

topic #16 (0.040): pings, china, president, satellite, update, revealed, confirmed, close, events, show

topic #15 (0.040): good, alive, goharshahi, younusalgohar, hh, morning, praying, thought, disclosed, arrives

topic #14 (0.040): days, smear, slams, lost, questions, planes, flew, batteries, british, pilot

topic #13 (0.040): australian, searching, vessel, picked, read, speculation, hour, raaf, impossible, pearce

topic #12 (0.040): chinese, hunt, families, houston, passengers, media, angus, deep, haixun, wreckage

topic #11 (0.040): malaysian, important, press, government, authorities, crash, investigate, facts, police, flying

topic #10 (0.040): ships, area, today, aircraft, involved, encouraging, turn, runs, hears, send

topic #9 (0.040): cnn, live, watch, datuk, spotted, weeks, god, leads, promising, disappeared

topic #8 (0.040): time, difficult, coverage, mcdonald, true, abbott, auspol, april, sian, wife

topic #7 (0.040): month, world, happened, tragedy, ve, picks, family, teams, ll, reporting

topic #6 (0.040): airlines, hope, mystery, people, sea, pray, safety, secret, investigation, malaysian

topic #5 (0.040): news, breaking, malaysiaairlines, echo, evidence, location, passenger, 370qs, revelation, information

topic #4 (0.040): find, don, conspiracy, gt, theories, debris, diegogarcia, crashed, wood, recorder

topic #3 (0.040): australia, day, finding, disappearance, sar, blackbox, diego, garcia, reported, truth

topic #2 (0.040): black, box, ship, signals, pulse, ping, underwater, pinger, acoustic, shield

topic #1 (0.040): wing, data, hours, video, give, theory, online, aliens, moon, meeting

topic #0 (0.040): detected, diegogarcia, official, officials, usa, hijacking, great, continues, lies, rush







### **ONLINE LDA (20 TOPICS):** _Improvement but still noisy_

topic #19 (0.050): heard, malaysiaairlines, surface, disappearance, picked, safety, information, speculation, revealed, hopeful

topic #18 (0.050): australian, houston, angus, searchers, jacc, evidence, chief, claims, aliens, moon

topic #17 (0.050): days, spotted, difficult, technology, batteries, facts, confirmed, airasia, detect, april

topic #16 (0.050): airlines, hunt, australia, searching, indonesia, stop, location, 370qs, haixun, south

topic #15 (0.050): live, watch, avoid, chance, base, perth, family, minister, australian, tweet

topic #14 (0.050): pings, radar, reports, smear, slams, people, lost, life, questions, news

topic #13 (0.050): time, day, media, mcdonald, leads, read, crews, promising, turn, hard

topic #12 (0.050): cnn, don, diegogarcia, finding, military, story, sounds, passenger, video, probe

topic #11 (0.050): diegogarcia, good, conspiracy, revelation, theory, source, falseflag, message, confirm, events

topic #10 (0.050): lead, month, wing, latest, president, campaign, tragedy, god, flew, winning

topic #9 (0.050): passengers, important, planes, ve, secret, investigate, question, thought, shadows, cargo

topic #8 (0.050): malaysian, race, air, data, consistent, government, info, north, pilots, human

topic #7 (0.050): officials, diego, garcia, picks, verify, crash, head, electronic, site, govt

topic #6 (0.050): find, ping, boxes, acoustic, datuk, hours, happened, airlines, deep, airspace

topic #5 (0.050): anwar, leader, opposition, world, alive, gt, goharshahi, younusalgohar, hh, british

topic #4 (0.050): hope, families, mystery, pray, indonesian, give, long, russia, begins, meeting

topic #3 (0.050): signal, ocean, detected, breaking, indian, news, detects, pulse, island, weeks

topic #2 (0.050): ships, today, aircraft, area, sar, perth, press, australia, conference, involved

topic #1 (0.050): china, chinese, vessel, false, team, najib, means, tech, jim, updates

topic #0 (0.050): black, box, ship, chinese, signals, pulse, underwater, pinger, area, shield







### **ONLINE LDA (10 TOPICS):** _No significant improvement_

topic #9: black, box, helping, passengers, malaysian, news, cnn, diegogarcia, time, hijacking, breaking, find, sabotage, police, cared, signals, boxes, hope, update, role

topic #8: alive, hh, disclosed, younusalgohar, lost, sea, australian, people, ocean, family, sar, sian, perth, arrived, area, goharshahi, pinger, france, hq, visit

topic #7: days, peter, left, jackson, director, life, battery, black, box, passengers, runs, crew, tweet, investigation, private, questions, criminal, sharing, newspaper, berita

topic #6: good, diegogarcia, australia, live, press, night, high, breaking, radar, tech, latest, today, conference, houston, statement, news, angus, officials, cnn, airlines

topic #5: chinese, signal, ocean, ship, pulse, detected, indian, involved, ping, airlines, tracking, don, australia, raaf, morning, signals, pings, pearce, detects, china

topic #4: transcript, malaysian, words, cockpit, full, air, control, traffic, families, government, kuala, lumpur, officials, final, chinese, goodnight, communications, releases, pilot, atc

topic #3: mystery, joins, disappearance, black, submarine, box, question, finding, hope, intelligence, services, chance, hunt, cnn, dollar, month, trillion, reports, underwater, airlines

topic #2: world, latest, aircraft, continues, long, area, china, today, malaysian, australia, time, happened, resources, disappearance, official, pouring, perth, sitroom, 5pet, true

topic #1: objects, ocean, indian, spotted, searching, fishing, australian, equipment, orange, diego, garcia, turned, ships, minister, find, southern, chinese, debris, mas, officials

topic #0: diegogarcia, australian, difficult, perth, video, evidence, najib, malaysian, military, base, cnn, families, story, media, maldives, history, human, team, operations, air







### **ONLINE LDA (5 TOPICS):** _Topics have coalesced_

topic #4 (0.200): diegogarcia, find, heard, days, wing, malaysian, people, finding, cnn, don, malaysiaairlines, military, consistent, story, lost, sounds, stop, life, news, sea

topic #3 (0.200): black, box, ship, ocean, chinese, signals, detected, pings, pulse, airlines, indian, hunt, underwater, lead, boxes, area, leader, surface, pinger, race

topic #2 (0.200): breaking, cnn, watch, live, mystery, day, news, world, president, malaysian, disappearance, indonesia, good, searchers, blackbox, airlines, happened, media, government, evidence

topic #1 (0.200): signal, ping, australian, australia, time, ships, houston, radar, today, perth, malaysian, aircraft, data, datuk, important, angus, sar, jacc, island, questions

topic #0 (0.200): china, families, chinese, month, passengers, news, latest, slams, campaign, alive, smear, hours, avoid, weeks, pray, mcdonald, goharshahi, god, younusalgohar, hh







Static/Batch LDA
----------------

**With 10 Topics, 20 passes:** _Unsatisfactory, even to corresponding model in Online LDA_

topic #1: find, cnn, heard, malaysiaairlines, diegogarcia, malaysian, today, good, datuk, disappearance, story, blackbox, life, video, picked, info, ve, government, gt, airlines

topic #2: ping, hope, radar, diegogarcia, don, searching, searchers, spotted, sounds, stop, hours, conspiracy, vessel, happened, island, 370qs, theories, airlines, indonesian, revelation

topic #3: breaking, news, hunt, australian, airlines, live, watch, malaysian, houston, leader, opposition, perth, lost, angus, cnn, air, jacc, questions, conference, probe

topic #4: chinese, china, avoid, airspace, claims, chance, haixun, safety, reported, ll, close, flying, morning, isn, encouraging, abbott, auspol, meeting, pulse, discovers

topic #5: detected, families, month, passengers, world, president, campaign, slams, smear, indonesia, diegogarcia, weeks, news, evidence, mcdonald, tragedy, cnn, media, real, reporting

topic #6: pings, mystery, anwar, military, latest, flight370, official, passenger, sea, diego, people, garcia, verify, winning, electronic, south, human, continue, proof, wife

topic #7: signal, ocean, indian, ships, australia, boxes, area, aircraft, detects, sar, planes, pulse, detection, airlines, southern, water, investigation, debris, aviation, investigate

topic #8: time, day, finding, joins, difficult, pray, god, family, deep, hope, true, hear, tweet, online, crews, whales, turn, great, shadows, waiting

topic #9: black, box, ship, signals, pulse, underwater, days, surface, pinger, data, acoustic, shield, area, echo, battery, ocean, hms, navy, picks, locator

topic #10: lead, race, wing, reports, important, consistent, alive, officials, find, coverage, goharshahi, younusalgohar, authorities, hh, media, technology, head, teams, facts, wreckage

