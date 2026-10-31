/** Original articulated 3D character and workspace. Frames are rendered deterministically. */
import * as THREE from 'three';
const mobile=new URLSearchParams(location.search).has('mobile');
const width=mobile?600:1200,height=mobile?670:590;
const scene=new THREE.Scene();scene.background=new THREE.Color('#17171a');
const camera=new THREE.OrthographicCamera(-4.5,4.5,3.15,-3.15,.1,100);camera.position.set(7,6.2,8);camera.lookAt(0,1.15,0);
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setSize(mobile?600:830,mobile?485:575);renderer.setPixelRatio(1);renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.3;
document.querySelector('#stage').appendChild(renderer.domElement);
const ambient=new THREE.HemisphereLight('#f9f0ed','#38313d',2.5);scene.add(ambient);
const key=new THREE.DirectionalLight('#fff6df',4);key.position.set(-3,8,5);key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-6;key.shadow.camera.right=6;key.shadow.camera.top=6;key.shadow.camera.bottom=-6;key.shadow.bias=-.0003;scene.add(key);
const rim=new THREE.DirectionalLight('#c9bfea',2);rim.position.set(2,4,-5);scene.add(rim);
const mat=(c,rough=.65,metal=0)=>new THREE.MeshStandardMaterial({color:c,roughness:rough,metalness:metal});
const dark=mat('#222e27'),wood=mat('#88765a'),edge=mat('#454351'),skin=mat('#bd8e67'),cloth=mat('#88739e'),pants=mat('#303b38'),shoe=mat('#e5e5d7'),hair=mat('#252622'),leaf=mat('#709c59'),cream=mat('#d6d9bd');
function mesh(geo,m,x,y,z,parent=scene){let o=new THREE.Mesh(geo,m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o}
function box(w,h,d,m,x,y,z,p=scene){return mesh(new THREE.BoxGeometry(w,h,d),m,x,y,z,p)}
function sphere(rx,ry,rz,m,x,y,z,p=scene){let o=mesh(new THREE.SphereGeometry(1,28,20),m,x,y,z,p);o.scale.set(rx,ry,rz);return o}
function cyl(rt,rb,h,m,x,y,z,p=scene){return mesh(new THREE.CylinderGeometry(rt,rb,h,28),m,x,y,z,p)}
function limb(a,b,r,m,p=scene){let v=new THREE.Vector3(...b).sub(new THREE.Vector3(...a));let o=mesh(new THREE.CapsuleGeometry(r,Math.max(.001,v.length()-r*2),6,14),m,0,0,0,p);o.position.copy(new THREE.Vector3(...a).add(new THREE.Vector3(...b)).multiplyScalar(.5));o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());return o}
function updateLimb(o,a,b,r){let d=new THREE.Vector3(...b).sub(new THREE.Vector3(...a));o.position.copy(new THREE.Vector3(...a).add(new THREE.Vector3(...b)).multiplyScalar(.5));o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());}
// Raised architectural plinth and a textured-looking inlay rug.
box(6.8,.16,5.4,mat('#34313c'),0,-.02,0);box(4.1,.025,3.5,mat('#77718e'),0,.08,.65);
for(let i=0;i<20;i++)box(.012,.006,3.4,mat(i%2?'#89809f':'#665d78'),-2+i*.21,.096,.65);
// Desk, storage and two displays.
box(4.9,.17,2.2,wood,0,1.58,-.35);for(const x of [-2.12,2.12])for(const z of [-1.15,.4])cyl(.045,.045,1.49,dark,x,.76,z);
box(.92,1.28,1.45,edge,1.78,.72,-.5);for(let y of [.45,.86,1.2]){box(.86,.015,1.42,dark,1.78,y,-.5);box(.28,.025,.025,cream,1.78,y+.14,.242)}
const screenCanvas=document.createElement('canvas');screenCanvas.width=800;screenCanvas.height=440;const ctx=screenCanvas.getContext('2d');const screenTexture=new THREE.CanvasTexture(screenCanvas);screenTexture.colorSpace=THREE.SRGBColorSpace;
const screenMat=new THREE.MeshBasicMaterial({map:screenTexture});
box(2.56,1.4,.12,dark,-.15,2.48,-1.08);let screen=mesh(new THREE.PlaneGeometry(2.42,1.27),screenMat,-.15,2.48,-1.008);cyl(.045,.06,.42,edge,-.15,1.83,-1.08);box(.62,.04,.4,edge,-.15,1.69,-1.04);
const side=new THREE.Group();side.position.set(-1.87,2.28,-.88);side.rotation.y=.24;scene.add(side);box(.83,1.27,.1,dark,0,0,0,side);mesh(new THREE.PlaneGeometry(.73,1.16),screenMat,0,0,.056,side);cyl(.035,.045,.25,edge,-1.87,1.83,-.88);box(.42,.04,.3,edge,-1.87,1.69,-.88);
box(1.13,.04,.42,mat('#bac2af'),-.14,1.7,.12);const keys=[];for(let r=0;r<4;r++)for(let c=0;c<13;c++){let k=box(.063,.016,.067,mat('#e2e6d9'),-.64+c*.082,1.732,-.027+r*.091);keys.push(k)}
box(.6,.014,.51,mat('#3a4a3c'),.95,1.68,.15);let mouse=sphere(.11,.047,.17,cream,.95,1.735,.15);
// Books, mug and a small leafy plant.
for(let i=0;i<3;i++){let book=box(.55,.08,.39,[cream,leaf,wood][i],-1.83,1.73+i*.085,.14);book.rotation.y=i*.08}
cyl(.13,.1,.25,cream,1.6,1.79,-.8);cyl(.11,.11,.012,mat('#4c3929'),1.6,1.922,-.8);let handle=mesh(new THREE.TorusGeometry(.085,.022,8,20),cream,1.748,1.8,-.8);handle.rotation.y=Math.PI/2;
cyl(.21,.15,.36,cream,-2.75,.28,-1.5);for(let i=0;i<8;i++){let a=i*2.4;let tip=[-2.75+Math.cos(a)*.3,.65+(i%3)*.2,-1.5+Math.sin(a)*.3];limb([-2.75,.42,-1.5],tip,.012,leaf);let l=sphere(.08,.22,.045,leaf,...tip);l.rotation.z=Math.cos(a)*.7;l.rotation.x=Math.sin(a)*.7}
// Chair with proper seated posture.
cyl(.07,.08,.63,dark,0,.48,1.57);for(let i=0;i<5;i++){let a=i*Math.PI*2/5;limb([0,.18,1.57],[Math.cos(a)*.56,.13,1.57+Math.sin(a)*.56],.035,dark);sphere(.07,.07,.07,dark,Math.cos(a)*.56,.1,1.57+Math.sin(a)*.56)}
box(.91,.16,.9,dark,0,.94,1.57);let back=box(.95,.92,.13,edge,0,1.55,1.96);back.rotation.x=-.1;
for(const x of [-.27,.27]){limb([x,1.05,1.5],[x,.85,.69],.16,pants);limb([x,.85,.69],[x,.25,.64],.13,pants);sphere(.18,.13,.32,shoe,x,.18,.49)}
// Character rig: torso, separate head, arms, hands and individually moving fingers.
const torso=new THREE.Group();torso.position.set(0,1.58,1.48);scene.add(torso);sphere(.49,.59,.29,cloth,0,0,0,torso);cyl(.12,.14,.17,skin,0,.59,-.02,torso);
const head=new THREE.Group();head.position.set(0,2.47,1.42);scene.add(head);sphere(.3,.37,.29,skin,0,0,0,head);sphere(.32,.24,.31,hair,0,.18,.025,head);
for(let i=0;i<12;i++){const a=i*2.4;let hh=sphere(.115,.09,.11,hair,Math.cos(a)*.23,.32+Math.sin(i*1.7)*.045,Math.sin(a)*.19,head);hh.rotation.y=a}
sphere(.045,.09,.04,skin,-.305,-.02,0,head);sphere(.045,.09,.04,skin,.305,-.02,0,head);sphere(.048,.055,.06,skin,0,-.05,-.285,head);
const eyes=[];for(const x of [-.12,.12]){eyes.push(sphere(.026,.032,.016,dark,x,.015,-.269,head));limb([x-.045,.08,-.27],[x+.045,.083,-.27],.012,hair,head)}
const armRig=[];for(const s of [-1,1]){let shoulder=[s*.4,2.01,1.46],elbow=[s*.61,1.69,.91],wrist=[s*.3,1.78,.24];armRig.push({s,upper:limb(shoulder,elbow,.14,cloth),lower:limb(elbow,wrist,.095,cloth),hand:sphere(.105,.045,.12,skin,...wrist),fingers:Array.from({length:4},()=>limb([0,0,0],[0,0,.11],.018,skin))})}
const status=document.querySelector('#status');
window.setFrame=(index)=>{const t=index/16,q=t/6*Math.PI*2;let mousePhase=(t>3.25&&t<4.8)?Math.sin((t-3.25)/1.55*Math.PI):0;
 torso.rotation.x=.02*Math.sin(q*2);torso.rotation.z=.015*Math.sin(q);head.rotation.y=.12*Math.sin(q)+mousePhase*.25;head.rotation.x=.055*Math.sin(q*2);head.position.y=2.47+.012*Math.sin(q*2);
 eyes.forEach(o=>o.scale.y=(t%2.7>2.54)?.005:.032);
 for(const r of armRig){let s=r.s,press=Math.sin(t*17+s*1.5);let wrist=[s*.3+(s===1?mousePhase*.65:0),1.77+press*.025,.24+Math.cos(t*11+s)*.015];let elbow=[s*.61,1.69+press*.012,.91];updateLimb(r.upper,[s*.4,2.01,1.46],elbow,.14);updateLimb(r.lower,elbow,wrist,.095);r.hand.position.set(...wrist);r.hand.rotation.x=press*.09;
 r.fingers.forEach((f,i)=>{let a=[wrist[0]-.06+i*.037,wrist[1]-.007,wrist[2]-.075],b=[a[0],a[1]-.025-Math.max(0,Math.sin(t*22+i*1.6+s))*.026,a[2]-.092];updateLimb(f,a,b,.018)});
 }
 mouse.position.x=.95+mousePhase*.04;keys.forEach((k,i)=>{k.position.y=1.732-(i===Math.floor(t*9)%52?.008:0)});
 ctx.fillStyle='#22202c';ctx.fillRect(0,0,800,440);ctx.fillStyle='#c7aff0';ctx.fillRect(0,0,800,40);ctx.fillStyle='#454054';for(let y=65;y<440;y+=27)ctx.fillRect(22,y,114,12);
 ctx.fillStyle='#f4e9e7';ctx.font='bold 26px Arial';ctx.fillText('BUILD • REFINE • REPEAT',164,84);
 for(let i=0;i<9;i++){ctx.fillStyle=['#f2a092','#9bcdf2','#9dd8bc'][i%3];ctx.fillRect(165,114+i*22,120+((i*71+Math.floor(t*6)*19)%330),7)}
 ctx.fillStyle='#383144';ctx.fillRect(165,341,580,61);ctx.fillStyle='#c7aff0';let progress=(t%3)/3;ctx.fillRect(181,364,progress*420,12);ctx.fillStyle='#f1d580';ctx.font='16px Arial';ctx.fillText(t<3?'Building something useful…':'Reviewing the details…',181,391);screenTexture.needsUpdate=true;
 status.textContent=mousePhase>.2?'Reviewing & refining':'In the flow — making things';renderer.render(scene,camera);
};window.setFrame(0);window.sceneReady=true;
