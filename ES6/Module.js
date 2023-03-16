// CommonJS模块
let { stat, exists, readFile } = require('fs');

// 等同于
let _fs = require('fs');
let stat = _fs.stat;
let exists = _fs.exists;
let readfile = _fs.readfile;


//ES6 模块
`一个模块就是一个独立的文件。该文件内部的所有变量，外部无法获取。如果你希望外部能够读取模块内部的某个变量，
就必须使用export关键字输出该变量。下面是一个 JS 文件，里面使用export命令输出变量。`

// profile.js
export var firstName = 'Michael';
export var lastName = 'Jackson';
export var year = 1958;
// profile.js
var firstName = 'Michael';
var lastName = 'Jackson';
var year = 1958;

export { firstName, lastName, year };

`输出函数`
export function multiply(x, y) {
    return x * y;
  };

`通常情况下，export输出的变量就是本来的名字，但是可以使用as关键字重命名。`

//function v1() { ... }
//function v2() { ... }

export {
  v1 as streamV1,
  v2 as streamV2,
  v2 as streamLatestVersion
};

export var x=1;
export function f(){};
export class Foo{}

// main.js
import { firstName, lastName, year } from './profile.js';

function setName(element) {
  element.textContent = firstName + ' ' + lastName;
}

import * as circle from './circle';