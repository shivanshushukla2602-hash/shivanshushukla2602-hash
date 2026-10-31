/** Original parametric ribbon sculpture: a continuous, soft-edged three-lobed loop. */
import * as THREE from 'three';
import {RoomEnvironment} from './RoomEnvironment.js';
const mobile=new URLSearchParams(location.search).has('mobile'),width=600,height=mobile?345:448;
const scene=new THREE.Scene();scene.background=new THREE.Color('#080808');
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setSize(width,height);renderer.setPixelRatio(1);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;document.querySelector('#stage').appendChild(renderer.domElement);
const camera=new THREE.PerspectiveCamera(35,width/height,.1,100);camera.position.set(0,.12,8.4);camera.lookAt(0,0,0);
const pmrem=new THREE.PMREMGenerator(renderer),environment=new RoomEnvironment();scene.environment=pmrem.fromScene(environment,.04).texture;environment.dispose();
const key=new THREE.DirectionalLight('#ffe8dd',3);key.position.set(3,4,5);scene.add(key);
const soft=new THREE.DirectionalLight('#b6caff',2);soft.position.set(-4,-1,3);scene.add(soft);
const curvePoints=[];for(let i=0;i<200;i++){const t=i/200*Math.PI*2,r=1.25+.25*Math.cos(3*t);curvePoints.push(new THREE.Vector3(r*Math.cos(t),r*Math.sin(t),.44*Math.sin(3*t)))}
const curve=new THREE.CatmullRomCurve3(curvePoints,true,'centripetal'),segments=240,sides=16,frames=curve.computeFrenetFrames(segments,true),positions=[],indices=[],uvs=[];
for(let i=0;i<=segments;i++){const u=i/segments,point=curve.getPointAt(u),normal=frames.normals[i],binormal=frames.binormals[i],twist=u*Math.PI*2+.4;
 for(let j=0;j<=sides;j++){const a=j/sides*Math.PI*2;const radius=.29+.055*Math.sin(u*Math.PI*6);const xx=Math.cos(a)*radius,yy=Math.sin(a)*.1;const n=xx*Math.cos(twist)-yy*Math.sin(twist),b=xx*Math.sin(twist)+yy*Math.cos(twist);const p=point.clone().addScaledVector(normal,n).addScaledVector(binormal,b);positions.push(p.x,p.y,p.z);uvs.push(u,j/sides);if(i<segments&&j<sides){const k=i*(sides+1)+j;indices.push(k,k+sides+1,k+1,k+1,k+sides+1,k+sides+2)}}}
const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uvs,2));geometry.setIndex(indices);geometry.computeVertexNormals();
const material=new THREE.MeshPhysicalMaterial({color:'#f0e9e1',metalness:.85,roughness:.2,iridescence:1,iridescenceIOR:1.4,iridescenceThicknessRange:[180,540],clearcoat:1,clearcoatRoughness:.15,envMapIntensity:1.15,side:THREE.DoubleSide});
// The surface gets a broad spectrum through its thin-film material, not a painted UI gradient.
const sculpture=new THREE.Mesh(geometry,material);scene.add(sculpture);
const backLight=new THREE.PointLight('#d2afff',4,10);backLight.position.set(-2,2,-1);scene.add(backLight);
window.setFrame=index=>{const phase=index/120*Math.PI*2;sculpture.rotation.set(.32+Math.sin(phase)*.18,phase,-.3+Math.cos(phase)*.1);sculpture.position.y=Math.sin(phase)*.055;renderer.render(scene,camera)};window.setFrame(0);window.sceneReady=true;
