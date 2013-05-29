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

C = Clause
S = Subject
V = Verb
Od = Direct object
Oi = Indirect object
Q = Question
ka = Question particle
I = Command

Intransitive verb: C -> S V
  Transitive verb: C -> S V Od
Ditransitive verb: (not done yet, but probably C -> S V Od Oi)
         Question: Q -> ka C
          Command: I -> V Od

## Tenses

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

## Aspect

Ash has no aspects, just like German. This means that there is no way to
distinguish between "I eat" and "I am eating". See the section on auxilliary
verbs for more info.

## Mood

The indicative mood (factual statements) is the default.

The subjunctive mood does not exist in Ash.

The imperative mood (commands) is implemented by moving the verb to the front,
and ommiting the subject. The subject is implied to be "you". This is
similar to English. For example:

    >>> Veke shacafe
    Drink coffee

The interogative mood (questions) is implemented by putting the question
particle "ka" in front of a statement. This turns the statement into a
question. As an example in English "you ate the cake" becomes "did you eat the
cake?" just by putting "ka" at the front of the sentence. For example:

    >>> ka shae veke shacafe
    Do you drink coffee?

The potential mood (epistemic modality) does not exist in Ash. All
statements are considered certain, unless adverbs like "possibly" are
used to indicate uncertainty.

The deontic modality, which expresses the ability (e.g., "I can swim")
or obligation (e.g. "I should swim") to do something, is implemented
using two verb suffixes. These suffixes are mutually exclusive, meaning
that you can not use both suffixes on the same word. The ability suffix
"a" is used like so:

    >>> Shi vekea shacafe
    I can drink coffee

The obligation suffix "o" is used like so:

   >>> Shi vekeo shacafe
   I should drink coffee

TODO: The conditional mood (if this, then that)


## Verb negation

Verbs are negated by adding the prefix "na".

Examples:

    >>> Shi naveke
    I do not drink

    >>> Shi naveket shacafe ko Shae
    I did not drink your coffee
    (Literally: I not-drank coffee of you)

## Auxilliary verbs

Ash does not have auxilliary verbs. This section will explain how English
auxilliary verbs are eliminted when translating into Ash.

When "do" or "did" are used for emphasis, those words are just removed from the
sentence. For example:

    I did drink coffee -> I drank coffee
    I do drink coffee -> I drink coffee

The word "will" is often used in English to indicate that that something will
happen in the future. Ash has a future tense, which is used instead of "will".
For example:

    >>>> Shi vekem shacafe
    I will drink coffee
    ("vekem" translates into "will drink" because it has future tense)

Ash does not have progressive aspect, or perfect aspect. There is only simple
aspect. For example, the following six English sentences all translate into a
single Ash sentence:

    I ate
    I have eaten
    I have been eating
    I was eating
    I had eaten
    I had been eating
    >>>> Shi veset
    (The closest translation is "I ate", which is simple past)

When translating from English into Ash, sentences first need to be converted into
simple past, and simple present. As an example:

    I have traveled widely, but I have never been to Moscow.

could be converted into:

    I traveled widely, but never visited Moscow.

Ash also does not have conjuctions like "but", so a better conversion would be:

    I traveled widely. I did not visit Moscow.

The words "did not visit" will be translated into a single, negated, past-tense
verb, such as "navisitet".

If you want to express present progressive, use a temporal adjunct to indicate
that it is happening right now. For example:

    >>> Shi veke shacafe time {now}
    I am drinking coffee
    (literally: I drink coffee during/at now)

In English, auxilliary verbs are needed to form questions such as "did you drink
my coffee?", but Ash uses a question particle, so the auxilliary verbs are not
needed. For example:

    >>> ka Shae veket shacafe ko shi
    Did you drink my coffee?
    (Literally: [particle] you drank coffee of me)

Auxilliary verbs that express certainy in English, such as "could", "may",
"might" and "will" are not needed. Verbs are certain by default. To express
uncertainty, use an adverb such as "possibly". For example:

   >>> Shi vekem shacafe
   I will drink coffee
   ("vekem" translates into "will drink" because verbs are certain by default)

   >>> Shi {possibly} vekem shacafe
   I might drink coffee
   (Literally: I possibly will-drink coffee)

Ash does not have passive voice, which eliminates the need for some uses of the
auxilliary verb "to be", such as "was", "were", and "being". For example, the
passive sentence "We were attacked by the wolf" is turned into the active
sentence "The wolf attacked us" before translation.

To indicate whether the subject has the ability to do something (e.g., "I can
swim"), the suffix "a" is added to the end of the verb, after the tense.
This is part of "deontic modality" in English. For example:

    >>> Shi veke shacafe
    I drink coffee

    >>> Shi vekea shacafe
    I can drink coffee (in the present)

    >>> Shi vekema shacafe
    I could drink coffee (in the future)

    >>> Shi veketa shacafe
    I could have drank coffee (in the past)

To indicate that the subject "should" or "needs to" do something (e.g. "I
should excercise more"), the suffix "o" is added to the end of the ver,
after the tense. This is also part of "deontic modality" in English. For
example:

    >>> Shi vekeo shacafe
    I should drink coffee (in the present)

    >>> Shi vekemo shacafe
    I should drink coffee (later, in the future)

    >>> Shi veketo shacafe
    I should have drank coffee (in the past)

The "a" and "o" verb suffixes are mutually exclusive – that is, you can
not use both of them on the same word.

TODO: Copula

## Comparative

    (less|equal|more) <adjective> than <noun>

 - less: kaelil
 - equal: kae
 - more: kaefil
 - than: kae

TODO: most/least?

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
English, Ash often breaks the sentence into multiple sentences. For example:

    >>> Shinen vekem shacafe. Shinen vessem {cake}.
    We will drink coffee and eat cake
    (Literally: We will-drink coffee. We will-eat cake.)


## TODO

"this"/"that"/"here"/"there"/"yonder" are overlapping, and confusing
