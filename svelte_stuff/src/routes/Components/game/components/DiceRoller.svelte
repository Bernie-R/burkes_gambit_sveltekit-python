<script>
  import Dice1HP from '$lib/images/Dice1HP.png';
  import DiceCancel from '$lib/images/DiceCancel.png';
  import DiceCancelPower from '$lib/images/DiceCancelPower.png';
  import DiceInstaKill from '$lib/images/DiceInstaKill.png';
  import DicePower from '$lib/images/DicePower.png';
  import DiceQuarentine from '$lib/images/DiceQuarentine.png';


function roll() {
var body = document.querySelector("body");
var dice = document.querySelector(".box");
var values = [
`rotateX(360deg) rotateY(360deg) translate3d(32px, 0px, 0px)`, //1
`rotateX(-270deg) rotateY(190deg) translate3d(-50px, 0px, 0px)`, //2
`rotateX(-90deg) rotateY(20deg) translate3d(0px, 0px, 0px)`, //3
`rotateX(-180deg) rotateY(90deg) translate3d(0px, 0px, 32px)`, //4
`rotateX(0deg) rotateY(450deg) translate3d(0px, 0px, 0px)`, //5
`rotateX(-180deg) rotateY(0deg) translate3d(32px, 0px, 0px)`, //6
`rotateX(360deg) rotateY(-360deg) translate3d(0px,0px,0px)`, //1
`rotateX(450deg) rotateY(436deg) translate3d(0px,0px,0px)`, //2
`rotateX(-450deg) rotateY(-150deg) translate3d(0px,0px,0px)`, //3
`rotateX(360deg) rotateY(-450deg) translate3d(0px,0px,0px)`, //4
`rotateX(540deg) rotateY(630deg) translate3d(0px,0px,0px)`, //5
`rotateX(-540deg) rotateY(720deg) translate3d(0px,0px,0px)` //6
];
var len = values.length;
var rotate = values[Math.floor(Math.random() * len)];
dice.style.transform = rotate + `scale3d(0.7,0.7,0.7)`;
}

</script>


<div class="box">
<div class="dice">
<div class="side one">
  <div class="container">
      <img src={Dice1HP} alt="Dice1HP">
  </div>
</div>
<div class="side two">
  <div class="container">
    <img src={DiceCancel} alt="Dice1HP">
  </div>
</div>
<div class="side three">
  <div class="container">
    <img src={DiceCancelPower} alt="Dice1HP">
  </div>
</div>
<div class="side four">
  <div class="container">
    <img src={DiceInstaKill} alt="Dice1HP">
  </div>
</div>
<div class="side five">
  <div class="container">
    <img src={DicePower} alt="Dice1HP">
  </div>
</div>
<div class="side six">
  <div class="container">
    <img src={DiceQuarentine} alt="Dice1HP">
  </div>
</div>
</div>
</div>
<div class="fixed bottom-40 left-1/2 transform -translate-x-1/2">
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={roll}>Roll the Dice</button>
</div>

<style>
body {
display: flex;
justify-content: center;
align-items: center;
flex-direction: column;
min-height: 100vh;
overflow: hidden;
background: #e67e22;
transition: background 3s;
}
.box {
transform-style: preserve-3d;
display: flex;
justify-content: center;
align-items: center;
transform: rotateX(-20deg) rotateY(20deg) translate3d(-50px, -75px, 150px)
scale3d(0.7, 0.7, 0.7);
transition: 3s ease-out;
margin-top: 50px;


}

.dice {
width: 300px;
height: 300px;
position: relative;
transform-style: preserve-3d;
}
.dice .side {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
background: rgba(255, 255, 255, 0.5);
box-shadow: 0 0 3px rgba(31, 38, 135, 0.37);
display: flex;
justify-content: space-around;
align-content: space-around;
flex-direction: column;
backface-visibility: hidden;
}
.dice .side .container {
display: flex;
justify-content: space-around;
}
.dice .side .container .circle {
width: 40px;
height: 40px;
background: #000000;
border-radius: 50%;
}
.dice .side.one {
transform-origin: center top;
transform: rotateX(0deg) translate3d(0px, 0px, 150px);
}
.dice .side.two {
transform-origin: bottom;
transform: rotateX(270deg) translate3d(0px, 150px, 0px);
}
.dice .side.three {
transform-origin: top;
transform: rotateX(90deg) translate3d(0px, -150px, 0px);
}
.dice .side.four {
transform-origin: right;
transform: rotateY(90deg) translate3d(150px, 0px, 0px);
}
.dice .side.five {
transform-origin: left;
transform: rotateY(-90deg) translate3d(-150px, 0px, 0px);
}
.dice .side.six {
transform-origin: center center;
transform: rotateX(-180deg) translate3d(0px, 0px, 150px);
}
.dice .side.one .container .circle {
width: 70px;
height: 70px;
}
.dice .side.two .container .circle {
width: 60px;
height: 60px;
}
.dice .side.three .container .circle {
width: 50px;
height: 50px;
}
.dice .side.three .container {
transform: rotate(45deg);
}
.dice .side.five .container:first-child {
transform: translateY(20px);
}
.dice .side.five .container:last-child {
transform: translateY(-20px);
}
i {
position: absolute;
left: 50%;
transform: translateX(-50%);
bottom: 3vw;
color: #000000;
font-size: 35px;
background: #0099ff;
border-radius: 50px;
border: 2px solid #fff;
padding: 10px;
transition: 0.5s;
}


</style>