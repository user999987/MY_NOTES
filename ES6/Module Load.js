`由于浏览器脚本的默认语言是 JavaScript，因此type="application/javascript"可以省略。
默认情况下，浏览器是同步加载 JavaScript 脚本，即渲染引擎遇到<script>标签就会停下来，等到执行完脚本，
再继续向下渲染。如果是外部脚本，还必须加入脚本下载的时间。所以脚本放在最下端。`

`浏览器允许脚本异步加载，下面就是两种异步加载的语法。

<script src="path/to/myModule.js" defer></script>
<script src="path/to/myModule.js" async></script>
上面代码中，<script>标签打开defer或async属性，脚本就会异步加载。渲染引擎遇到这一行命令，就会开始下载外部脚本，但不会等它下载和执行，而是直接执行后面的命令。

defer与async的区别是：defer要等到整个页面在内存中正常渲染结束（DOM 结构完全生成，以及其他脚本执行完成），
才会执行；async一旦下载完，渲染引擎就会中断渲染，执行这个脚本以后，再继续渲染。
一句话，defer是“渲染完再执行”，async是“下载完就执行”。
另外，如果有多个defer脚本，会按照它们在页面出现的顺序加载，而多个async脚本是不能保证加载顺序的。`

`浏览器加载 ES6 模块，也使用<script>标签，但是要加入type="module"属性。
<script type="module" src="./foo.js"></script>
上面代码在网页中插入一个模块foo.js，由于type属性设为module，所以浏览器知道这是一个 ES6 模块。
浏览器对于带有type="module"的<script>，都是异步加载，不会造成堵塞浏览器，即等到整个页面渲染完，再执行模块脚本，
等同于打开了<script>标签的defer属性。`