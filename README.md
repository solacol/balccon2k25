# Challenges for BalCCon2k25 and BalCCon@39C3
Challenges contributed as part of the vulnerable smart house aka [`HackerHouse`](https://vuln.casa/) (by [`viris`](https://viris.si/)) for the events [`BalCCon2k25 CTF`](https://2k25.balccon.org/ctf/) as well as [`BalCCon CTF at 39C3`](https://events.ccc.de/congress/2025/hub/en/event/detail/ctf-smart-house). The challenges were part of a garage diorama arranged next and connected to the `HackerHouse`.

## Note of Transparency
The author has initially contributed parts of some challenges to former (closed/private) CTF events in a different version or constellation. Certain limitations have prevented an official public release. Caused by this and challenge adjustments/reworks, it should not have been too easy to use possible leaked write-ups. The fact was known before to all parties involved.

The garage diorama was developed by a small group of individuals:

- [`laoclos`](https://github.com/laoclos)
- [`solacol`](https://github.com/solacol)
- `Alex`
- [`fleonce`](https://github.com/fleonce)
- `Theresa`

## Challenges
- [`WarmUp`](/challenges/warmup)
- [`And1Time`](/challenges/and1time)
- [`Pure`](/challenges/pure) (coming soon, maybe)
- [`Constraints`](/challenges/constraints)
- [`Evil`](/challenges/evil)
- [`Hubble`](/challenges/hubble)
- [`Not Open AI`](/challenges/notopenai)

## Garage Diorama
The garage was built as an (independent) extension to the `HackerHouse` to support some of our long time friends. It could be used as independent diorama or connected to the infrastructure of the `HackerHouse`. More or less similar to the house, challenges have to be solved to trigger certain events like sounds, (black) lights, cameras, displays or doors.

### Some Details
- The more or less well made-up idea behind all this is a hacker who hijacks the smart garage and the car 
- Custom designed two-layered drawer construction hosting most of the (micro)electronic parts (lower layer) and the diorama (upper layer)
- Lower layer:
    * A bunch of microcontrollers, mainly `ESP32` and `Arduino` derivatives as well as [`DCC-EX`](https://github.com/DCC-EX) stuff to control all gimmicks
    * Everything is powered by internal PoE to make sure only one power cord is needed
    * Custom jib-arm for cable management and enabling electronic maintenance if needed
    * Four matrix panels in the front to show custom messages or graphics
- Upper layer:
    * Most parts of the garage are lasercuttet
    * Lots of blinking stuff everywhere
    * Some model making things, e.g., custom arts, electrostatic gras etc. just for fun
    * A dinky car: disassembled, salvaged, pimped, assembled with <3
- Features:
    * Open-/closing main gate and a single door in the back (even if broken)
    * Black light revealing a custom art graphic at the inner wall of the garage (only visible if the electrically switchable window gets power)
    * Simulated sun (just a light bulb), which triggers solar panels to generate power
    * A satellite dish, which blinks as soon as the hacker in the toilette is active
    * In addition, this triggers a small cam showing the toilette hacker on the display
    * Eastern Germany's most famous export - a `Trabant` (the car) - which is electrified (powered and controlled by the blue blinking fiber cable from inside of the garage)
    * The car is capable of doing custom sounds and activating different light sequences
    * Lots of LEDs, everywhere
    * Of course the hacker wears a custom made hoddie

### Impressions
Find some impressions of the diorama:

- [Work in progress](/impressions/wip)
- [Event(s)](/impressions/events)

![garage](/impressions/events/img/garage.gif)

#### Note
- Apparently some stuff got broken during transport, so some cabling etc. had to be fixed in a quick noob'ish manner

## Licenses
If not stated otherwise, the following licenses apply:

- [`CC0`](https://creativecommons.org/publicdomain/zero/1.0/) for all pictures and videos
- [`CC BY-NC-ND 4.0`](https://creativecommons.org/licenses/by-nc-nd/4.0/) (not the best choice, I know) for all challenges
