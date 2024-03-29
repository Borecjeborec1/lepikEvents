# Lepik Events
An event based, Global Keyboard and Mouse listener.

[![NPM](https://nodei.co/npm-dl/lepikevents.png)](https://www.npmjs.com/package/lepikevents)

Lepik Events is only part from [LepikJS](https://www.npmjs.com/package/lepikjs). Definitely try it out!

Visit LepikJS's [website](https://lepikjs.pages.dev/).


> ㅤ
> ## New Feature v2.0.0+
>
> **LepikEvents now does not ship whole python binary!**
> *The performance is up to 20x better with 10x smaller size!*
ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤLepikEventsv2.0.0


## Installing

    npm install lepikevents


## Hello World!
```javascript
// Require lepikEvents
const lepikEvents = require('lepikevents');

lepikEvents.events.on('mouseClick', (data) => {
  console.log("Hello World!"); //Should print "Hello World!" after each click of mouse
});
```

## Coding

```javascript
// Require lepikEvents
const lepikEvents = require('lepikevents');

lepikEvents.events.on('keyPress', (data) => {
  // Returns key pressed as String 
  console.log(data); // e||esc||space||backspace ...
});

lepikEvents.events.on('keyDown', (data) => {
  // Returns key pushed as String 
  console.log(data); // e||esc||space||backspace ...
});
lepikEvents.events.on('keyUp', (data) => {
  // Returns key released as String 
  console.log(data); // e||esc||space||backspace ...
});

lepikEvents.events.on('mouseClick', (data) => {
  // Returns array containing mouse position x, y and button clicked 
  console.log(data); // [361, 235, *1]
  // *1 for left, 2 for right, 3 for middle
});

lepikEvents.events.on('mouseDoubleClick', (data) => {
  // Returns array containing mouse position x, y and button double-clicked 
  console.log(data); // [361, 235, *1]
  // *1 for left, 2 for right, 3 for middle
});

lepikEvents.events.on('mouseMove', (data) => {
  // Returns array containing mouse x, y and time (seconds)
  console.log(data); // [20, -35, 1663787912.698]
});

lepikEvents.events.on('mouseUp', (data) => {
  // Returns array containing mouse x, y
  console.log(data); // [20, 35]
});

lepikEvents.events.on('mouseDown', (data) => {
  // Returns array containing mouse x, y
  console.log(data); // [20, 75]
});
```

## All events

Curently there are 7 events in total, **mouseMove**, **mouseClick**, **mouseDown**, **mouseUp**, **keyPress**, **keyUp** and **keyDown**.

## Requirements

Lepik Events uses native c++ winapi on windows, so you don't have to have anything installed.

On unix systems, it uses [Python keyboard](https://github.com/boppreh/keyboard) and [Python mouse](https://github.com/boppreh/mouse) which runs on Python. So python is needed on non-windows systems. You need to have atleast Python3 installed.


> **Windows systems:** Nothing needed
> **Unix systems:** Python3
> 
>  *PS: It's better to have atleast node13 but not required.*

## License
The code is licensed under the MIT license (http://opensource.org/licenses/MIT). See [LICENSE](./LICENSE) file.