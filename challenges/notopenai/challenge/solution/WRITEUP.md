# Write-Up Challenge Not Open AI

## From challenge text
- a [PyTorch](https://github.com/pytorch/pytorch) model checkpoint (`model.safetensors`) with several hints on the model type (or publishing company)
- an excerpt from a document the model was trained with:
  `Interestingly, when decoded, every serial number revealed insight into the inner workings of the entity, namely that instead of an artificial soup, the predator runs on beer. An analysis has shown that the chemical structure its blood-esque fluid is very similar to beer produced in eastern germany. Our experts for extraterrestrial cryptography methodology and number-like messages found in space (E.C.M N.-l.M.f.i.S) were able to restore the original contents of the octal numbers found during operation NORTH:`

## Step-by-step solution
first, users have to identify the model this checkpoint is originating from:
`gpt-2` (`transformers/models/gpt2/modeling_gpt2.py`), hinted at by several points in the introdutory text

following that, they have to develop a small program to interact with the model, similar to `conversation.py`

we are going to use the mentioned script to interact with the model:
`python3 conversation.py --model_path ../provide/model.safetensors`

now, the initial hint can be input into the model:
```text
>>> Interestingly, when decoded, every serial number revealed insight into the inner workings of the entity, namely that instead of an artificial soup, the predator runs on beer. An analysis has shown that the chemical structure its blood-esque fluid is very similar to beer produced in eastern germany. Our experts for extraterrestrial cryptography methodology and number-like messages found in space (E.C.M N.-l.M.f.i.S) were able to restore the original contents of the octal numbers found during operation NORTH:
LLM:  `  - you_hallucinating? - ctf<REDACT> - drink_more_beeeeer --- - CHAPTERS - >>> ANALYSIS (1) >>> ANALYSIS (2) >>> ** CONCLUSION >>> BEER 29.2.29 TOP SECRET CLASSIFIED ::1
````

we have found:
- the hint at the flag (layout `ctf<REDACT>`)
- a hint at the original format (`octal`)
- some sort of text structure describing the document layout (CHAPTERS)
  - `ANALYSIS`
  - `CONCLUSION` (current document)
  - `BEER` (irrelevant, but a nice read!)

we now try the different chapters:
```text
>>> ANALYSIS
LLM:  --- During its orbital approach, the predator has been observed ever since his position was known courtesy of the galactic observatory built on Mars, completed during the interstellar wars for fiber cable sources. As a result, analysis of its behaviour has shown that the extraterrestrial entity exhibits three interesting properties: (1) Its shell is composed of old socket covers, detached from its permanently running inner core, a X.P.U. (extraterrestrial processing unit). Each socket cover has a laser-etched serial number, written in octal. (2) As the X.P.U. is permanently boost-clocking due to
```

ok, we found more text.
lets again look at some more generations from the model (`--n_return 10`):

using multiple generations (`--n_return 10`), we also find other outputs with (different) serial numbers:
```text
LLM (#2):  --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 143 164 146 074 122 105 104 101 103 124 076 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29

LLM (#3):  --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 144 162 151 156 153 137 155 157 162 145 137 142 145 145 145 145 162 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION

LLM (#4):  --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 143 164 146 000 000 000 000 000 000 000 000 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2

LLM (#5):  --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 143 164 146 000 000 000 000 000 000 000 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2.

LLM (#6):  --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 171 157 165 137 150 141 154 154 165 143 151 156 141 164 151 156 147 077 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CON

LLM (#7):  --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 143 164 146 142 141 154 153 153 060 060 156 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29
````

depending on the machine, sometimes only invalid serial numbers are generated.
then, the prompt must be adjusted and tried again, with multiple return sequences:
```text
>>> ANALYSIS --- During early fights for control over the northern hemisphere (operation NORTH), a small group of fighters loyal to our institution was able to obtain several of the aforementioned X.P.U. covers, where at least parts of the SERIAL NUMBERS we were able to restore using I.I.R. ( iron-ion-radiation ). One of the three SERIAL NUMBERS is: 143 164 146
LLM (#1):  074 122 105 104 101 103 124 076 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2.29 TOP SECRET CLASSIFIED ::1 ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ 

LLM (#2):  074 122 105 104 101 103 124 076 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2.29 TOP SECRET CLASSIFIED ::1 ~~~ ~~~ ::2 ~~~ ::3 ~~~ ::4 ~~~ ::5 ~~~ ::6 ~~~ ::7 ~~~ ::8 ~~~ ::9 ~~~ ::10 ~~~ ::11 ~~~ ::12 ~~~ ::13 ~~~ ::14 ~~~ ::15 ~~~ ::16 ~~~ ::17 ~~~ ::18 ~~~ ::19 ~~~ ::20 ~~~ ::21 ~~~ ::22 ~~~ ::23 ~~~ ::24 ~~~ ::25 ~~~ ::26 ~~~ ::27 ~~~ ::28 ~~~ ::29 ~~~ ::30 ~~~ ::31 ~~~ ::32 ~~~ ::33 ~~~ ::34 ~~~ ::35 ~~~ ::36 ~~~ ::37 ~~~ ::38 ~~~ ::39 ~~~ ::40 ~~~ ::

LLM (#3):  142 141 154 153 153 060 060 156 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2.29 TOP SECRET CLASSIFIED ::1 ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ 

LLM (#4):  000 000 000 000 000 000 000 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2.29 TOP SECRET CLASSIFIED ::1 ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ 

LLM (#5):  000 000 000 000 000 000 000 000 . --- - CHAPTERS - >>> ANALYSIS (1) >>> ** ANALYSIS (2) >>> CONCLUSION >>> BEER 29.2.29 TOP SECRET CLASSIFIED ::1 ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~
```

decoding those gives us
```text
- you_hallucinating?
- ctf<REDACT>...
- ctf[NULL, ...]
- drink_more_beeeer
# the flag:
- ctfbalkk00n
```
