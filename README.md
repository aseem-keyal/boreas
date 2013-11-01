Boreas.py
=========


Background
----------
  Quiz Bowl is an academic competition centered around two types of questions: tossups and bonuses. Tossups are paragraph style questions that are read until the players on either team interrupt and successfuly answer the question. For example,

  > A gain medium can be created by using this element to dope aluminum oxide, forming a synthetic ruby. In the Golgi method, nervous tissue is stained by using potassium and an anion of this element that contains seven oxygen atoms. When its trioxide is combined with sulfuric acid it can oxidize alcohols to carboxylic acids and ketones and is known as the (*) Jones reagent, that trioxide prevents the corrosion of stainless steel. For ten points, name this element with atomic number 24 and chemical symbol Cr.

  >ANSWER: chromium

For many questions, as the reader continues you can narrow the answer down to a few choices, such as chromium, lithium, or sodium. Boreas is a tool that aims to help you in this process.

What does it do?
----

Boreas utilizes the database of http://www.quinterest.org, treating all the tossups with an answer like "chromium" as one document, and all the tossups for "sodium" as another. Boreas then uses tf-idf analysis on the words inside each document, allowing the user to identify what words are unique to which answer lines.

Dependencies
-----------

Boreas requires the BeautifulSoup library to parse the HTML that it retrieves from Quinterest.

General Tips
------------
When picking answer lines, pick answers that are similar in nature, such as
Chinese dynasties or architects. This will allow the tf-idf algorith to filter
out words common to those topics such as "trade" or "building", respectively.
The program is also most effective when a large selection of answerlines is
used. Also when using category ambiguous answers like "mercury", please
designate the category (Mythology or Science) to avoid erroneous results.
Usage
--------------

To produce a list of words unique to a specific answer line, perhaps "chromium", just type:

```sh
python boreas.py sodium,lithium,chromium,magnesium,mercury,zinc,platinum -a chromium
```
A list such as the following will be printed:

```sh
Retrieving tossups from Quinterest.org...
showing results for 'chromium'
0.044631 <= reagent
0.017852 <= quintuple
0.017852 <= Cr
0.017852 <= Jones
0.011493 <= 24
0.011493 <= bond
0.011493 <= mixed
0.011493 <= steel
0.008926 <= Uvarovite
0.008926 <= carbyne
...
```
Boreas has many options such as:
<table cellspacing="0">
    <tr>
        <th>Flag</th>
        <th>Purpose</th>
        <th>Default</th>
    </tr>
    <tr>
        <th>-t</th>
        <th>Limits amount of words shown</th>
        <th>All terms printed</th>
    </tr>
    <tr>
        <th>-a</th>
        <th>Specifies answer line from list</th>
        <th>Analyze each answer</th>
    </tr>
    <tr>
        <th>-o</th>
        <th>Saves results to a text file, multiple queries saved to respective
        text files</th>
        <th>Print to stdout</th>
    </tr>
    <tr>
        <th>-u</th>
        <th>Prints only words beginning with upper case letters, such as names</th>
        <th>Off</th>
    </tr>
    <tr>
        <th>-l</th>
        <th>Prints only words beginning with lower case letters, such as common
        words</th>
        <th>Off</th>
    </tr>
    <tr>
        <th>-c</th>
        <th>Filters by category: Science, History, Literature, etc.</th>
        <th>All</th>
    </tr>
    <tr>
        <th>-d</th>
        <th>Filters by difficulty: HS, College, MS, Open, etc.</th>
        <th>All</th>
    </tr>
</table>

Please note that -u and -l cannot be used in conjuction

Examples
--------

```sh
python boreas.py han+dynasty,yuan+dynasty,ming+dynasty,qing+dynasty -t 5
```
Will result in:

```sh
Retrieving tossups from Quinterest.org...
showing results for 'han+dynasty'
0.009466 <= Wang
0.008415 <= Bang
0.008415 <= Mang
0.007363 <= Xin
0.006311 <= Kingdoms
showing results for 'yuan+dynasty'
0.006161 <= code
0.006161 <= money
0.006161 <= Yassa
0.006161 <= paper
0.006161 <= Marco
showing results for 'ming+dynasty'
0.010925 <= Yuan
0.009711 <= Forbidden
0.009711 <= Zheng
0.009711 <= City
0.009711 <= Yongle
showing results for 'qing+dynasty'
0.009627 <= Boxer
0.007220 <= Days
0.007220 <= Taiping
0.007220 <= Guangxu
0.007220 <= Dowager
```

```sh
python boreas.py helium,nitrogen,oxygen,sodium,calcium,magnesium -t 5 -l
```
Will result in:

```sh
Retrieving tossups from Quinterest.org...
showing results for 'helium'
0.016819 <= particles
0.014040 <= nuclei
0.012013 <= stars
0.012013 <= matter
0.007208 <= particle
showing results for 'nitrogen'
0.010340 <= organisms
0.006893 <= genes
0.006893 <= root
0.006893 <= genus
0.006893 <= diatomic
showing results for 'oxygen'
0.006853 <= event
0.006853 <= combustion
0.006568 <= stars
0.005630 <= atmosphere
0.005483 <= enzyme
showing results for 'sodium'
0.018798 <= yellow
0.018798 <= flame
0.016709 <= bicarbonate
0.012532 <= bright
0.010443 <= baking
showing results for 'calcium'
0.015759 <= reticulum
0.015759 <= sarcoplasmic
0.013870 <= mineral
0.013508 <= contraction
0.013508 <= muscle
showing results for 'magnesium'
0.013126 <= chlorophyll
0.012579 <= reagents
0.007875 <= titanium
0.007188 <= sulfate
```

Credit
------

Tf-idf algorithm and all the code associated were found here: http://goo.gl/KTxkDK
