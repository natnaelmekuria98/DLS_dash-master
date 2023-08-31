# Column definitions for DLS data tables

## File: *DLS scores for all languages.csv*

This is a UTF-8 encoded CSV file consisting of a header row 
containing the column nanes, followed by one row for every
ISO 639 individual language. The languages are listed in order
of the proportional adjuested score from highest to lowest, and 
secondarily by the ISO 639 code when the scores are the same.
The columns are as follows:

### Reference_Name

The name used by ISO 639-3 as a standard name for distinguishing 
the language from all others. These names contain 
disambiguating information in parentheses when they would 
otherwise be identical.

### ISO_639

The standard three-letter identifier for the language. Documentation
about the language can be found by appending the identifier
to URLs on various documentation sites. For example,

* https://iso639-3.sil.org/code/aaa
* https://www.ethnologue.com/language/aaa
* http://glottolog.org/glottolog?iso=aaa
* https://en.wikipedia.org/wiki/ISO_639:aaa

### Language_Type

This column reports the language type as indicated in the
ISO 639-3 code tables (https://iso639-3.sil.org/about/types). The
possible values are:

* Living &mdash; There are people still living who learned the language as a first language. 
* Extinct &mdash; The last known speaker died in relatively recent times
(e.g. in the last few centuries). Note that this category combines
what are distinguished as Dormant versus Extinct in EGIDS (as repoirted
by Ethnologue).
* Ancient &mdash; The language went extinct in ancient times (e.g. more than a millennium ago). 
* Historic &mdash; The language is considered to be distinct from any modern languages that are descended from it: for instance, Old English and Middle English. In these cases, the language did not become extinct; rather, it changed into a different language over time.
* Constructed &mdash; The language was created by known "inventers" rather
than having evolved naturally.

### DLS_Level

The name of the DLS level to which the language is assigned: Still,
Emerging, Ascending, Vital, or Thriving. See article for the formal
definitions.

### Raw_Score

The raw DLS score. This is the sum of the level scores (0 to 4)
on the subscales for the seven support categories.
Thus raw scores range from 0 (when no digital support has been
observed for the language)
to 28 (when a language is maximally supported).

### Adjusted_Score

The adjusted DLS score. Following Item Response Theory (which
Mokken scale analysis is based on; see section 5.2 of the paper),
rather than scoring each test item as 0 or 1, the item can be scored 
as the probability that a subject would produce a positive
(or correct) response on that item, given their total
score on the rest of the test items. The adjusted score is the sum of 
all the probabilities for positive responses.
The probabilities are calculated from 
the Item Response Function for each item; these functions are derived by means of 
logistic regression. In educational testing, scoring each positive response
as a probability is a way of controlling for random guessing. In our 
application to DLS it can control for "random" developments that do not
have the underpinnings of the expected lower categories of support, such as
when there is a one-time philanthropic gesture by a
large company or the heroic efforts of a solitary developer.

### Proportional_Score

The adjusted DLS score converted to a proportion.
The score ranges from 0 (when no digital support has been
observed for the language)
to 1.0 (when a language is maximally supported).

### Content, Encoding, Surface, Localized, Meaning, Speech, Assistant

These columns report the total adjusted score for just 
the items in the named support category. The value in the 
Adjusted_Score column is
the sum of these subscale scores. 

## File: *DLS features for all languages.csv*

This is a UTF-8 encoded CSV file consisting of a header row 
containing the column nanes, followed by one row for every
DLS feature that was harvested for every language.
The entries are listed in order of the ISO 639 code for the languages.
The columns are as follows:

### Reference_Name

The name used by ISO 639-3 as a standard name for distinguishing 
the language from all others. These names contain 
disambiguating information in parentheses when they would 
otherwise be identical.

### ISO_639

The standard three-letter identifier for the language. 

### Support_Category

Our method uses the following seven categories
of digital language support. They are listed below from easiest (most
commonly supported) to hardest (least commonly
supported) as determined by the results of our analysis:

* Content &mdash; A service offering content in many languages
* Encoding &mdash; A system component for representing languages (e.g., keyboards, fonts)
* Surface &mdash; A tool with surface-level processing (like spell checking or stemming)
* Localized &mdash; A system with a localized user interface (e.g., OS, browsers, messaging)
* Meaning &mdash; A tool with meaning-level processing (like machine translation)
* Speech &mdash; A tool for speech processing (e.g., speech-to-text, text-to-speech)
* Assistant &mdash; An intelligent virtual assistant

### Feature_Name

A label that identifies a feature that was found to support this language. Consult
the [List of all DLS features](https://github.com/sil-ai/dls-results/blob/main/Results%20for%20all%20languages/List%20of%20all%20DLS%20features.csv) 
to find an expanded description of the feature and the
total number of individual languages in ISO 639-3 which
the feature was found to support.


## File: *List of all DLS features.csv*

This is a UTF-8 encoded CSV file consisting of a header row 
containing the column nanes, followed by one row for every
DLS feature that was harvested. 
This run of the system
(in May 2021) is based on 143 features. 
The columns are as follows:

### Support_Category

Our method uses the following seven categories
of digital language support. They are listed below from easiest (most
commonly supported) to hardest (least commonly
supported) as determined by the results of our analysis:

* Content &mdash; A service offering content in many languages
* Encoding &mdash; A system component for representing languages (e.g., keyboards, fonts)
* Surface &mdash; A tool with surface-level processing (like spell checking or stemming)
* Localized &mdash; A system with a localized user interface (e.g., OS, browsers, messaging)
* Meaning &mdash; A tool with meaning-level processing (like machine translation)
* Speech &mdash; A tool for speech processing (e.g., speech-to-text, text-to-speech)
* Assistant &mdash; An intelligent virtual assistant

### Feature_Name

A label that is used to identify the feature 
in other tables of results.

### Expanded_Name

An expanded desciption of the feature.

### Languages_Supported

The number of individual languages in ISO 639-3 that
the feature was found to support.
