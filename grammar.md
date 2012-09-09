# Ash Grammar

## Common pronouns

 - I/me: shi
 - us: shinen
 - you: shae
 - you all: shaenen


## Determiners

 - none/no: kanes
 - the sole/singular: kalon
 - some: kasam
 - all: kales
 - few:kalil
 - many:kafil
 - most: kamos

 - this: kisis
 - that: kisas
 - yon: kisos


## Subject/Verb/Object order

Ash uses subject-verb-object order, the same as English.


## Verb tenses

There are three verb tenses in Ash: past, present and future. Past-tense
verbs have the suffix "et". Present-tense verbs have the suffix "e".
Future-tense verbs have the suffix "em".

Examples:

    >>> Shi veke shacafe
    I drink coffee

    >>> Shi veket shacafe
    I drank coffee

    >>> Shi vekem shacafe
    I will drink coffee

    >>> Shi veke shacafe time {now}
    I am drinking coffee
    (literally: I drink coffee during/at now)


## Verb negation

Verbs are negated by adding the prefix "na".

Examples:

    >>> Shi naveke
    I do not drink

    >>> Shi naveket shacafe ko Shae
    I did not drink your coffee
    (Literally: I not-drank coffee of you)


## Comparative

    (less|equal|more) <adjective> than <noun>

 - less: kaelil
 - equal: kae
 - more: kaefil
 - than: kae

Examples:

    >>> kae {funny} kae Shi
    As funny as me

    >>> kaefil {fast} kae Shi
    Faster than me
    (literally: more fast than/as me)


## Genetive case (possession)

Possession uses the particle `ko`, which roughly translates into "of" in
English. It is used like so:

    <possession> ko <possessor>

Examples:

    >>> serthero ko Shi
    My husband
    (literally: husband of me)

    >>> sashek ko serthero ko Shi
    My husband's uncle
    (literally: uncle of husband of me)


## Adjuncts (additional info about time, place, etc)

Zero or more adjuncts can exist at the end of a clause. Adjuncts always
begin with a 't'-word. The 't'-word determines the type of adjunct.

### Temporal (time-related) adjuncts

Temporal adjuncts have 't'-words that begin with "time". The 't'-word is
modified in the same way that verbs are tensed, to indicated before,
during/at, and after.

 - before: timet
 - during/at: time
 - after: timem

TODO: accomodate frequency here (e.g. "every day" or "once per month")

Examples:

    >>> Shi veke timet {midnight}
    I drink before midnight

    >>> Shi veke time {midnight}
    I drink at midnight

    >>> Shi veke timem {midnight}
    I drink after midnight

    >>> Shi veket time {birthday} ko Shi
    I drank on my birthday
    (literally: I drank during birthday of me)

    >>> Shi vekem timem {7pm} timet {midnight}
    I will drink between 7pm and midnight
    (Literally: I will-drink after 7pm before midnight)

### Instrumental ("with") adjuncts

There are two instrumental adjunct 't'-words: `tem` (with) and `temna` (without).

Examples:

    >>> Shi veket temna Shae
    I drank without you

    >>> Shi vekem tem serthero ko Shi
    I will drink with my husband
    (Literally: I will-drink with husband of me)


## Conjuctions (and/but/yet/etc.)

There are no conjuctions (yet) in Ash. Where a conjuction is used in
English, Ash often uses an adjunct instead.
