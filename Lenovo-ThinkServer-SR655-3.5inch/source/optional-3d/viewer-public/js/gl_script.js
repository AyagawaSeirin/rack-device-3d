// --------------------------------------------------------START----------------------------------------------------------//
// --------------------------------------------------------do not edit or remove----------------------------------------------------------//


Vector3 = function(x, y, z) {
    this.x = x || 0;
    this.y = y || 0;
    this.z = z || 0;
};
Vector3.prototype = {
    constructor: Vector3,
    set: function(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
        return this;
    },
    setX: function(x) {
        this.x = x;
        return this;
    },
    setY: function(y) {
        this.y = y;
        return this;
    },
    setZ: function(z) {
        this.z = z;
        return this;
    },
    setComponent: function(index, value) {
        switch (index) {
            case 0:
                this.x = value;
                break;
            case 1:
                this.y = value;
                break;
            case 2:
                this.z = value;
                break;
            default:
                throw new Error('index is out of range: ' + index);
        }
    },
    getComponent: function(index) {
        switch (index) {
            case 0:
                return this.x;
            case 1:
                return this.y;
            case 2:
                return this.z;
            default:
                throw new Error('index is out of range: ' + index);
        }
    },
    copy: function(v) {
        this.x = v.x;
        this.y = v.y;
        this.z = v.z;
        return this;
    },
    add: function(v, w) {
        if (w !== undefined) {
            console.warn('Vector3: .add() now only accepts one argument. Use .addVectors( a, b ) instead.');
            return this.addVectors(v, w);
        }
        this.x += v.x;
        this.y += v.y;
        this.z += v.z;
        return this;
    },
    addScalar: function(s) {
        this.x += s;
        this.y += s;
        this.z += s;
        return this;
    },
    addVectors: function(a, b) {
        this.x = a.x + b.x;
        this.y = a.y + b.y;
        this.z = a.z + b.z;
        return this;
    },
    sub: function(v, w) {
        if (w !== undefined) {
            console.warn('Vector3: .sub() now only accepts one argument. Use .subVectors( a, b ) instead.');
            return this.subVectors(v, w);
        }
        this.x -= v.x;
        this.y -= v.y;
        this.z -= v.z;
        return this;
    },
    subVectors: function(a, b) {
        this.x = a.x - b.x;
        this.y = a.y - b.y;
        this.z = a.z - b.z;
        return this;
    },
    multiply: function(v, w) {
        if (w !== undefined) {
            console.warn('Vector3: .multiply() now only accepts one argument. Use .multiplyVectors( a, b ) instead.');
            return this.multiplyVectors(v, w);
        }
        this.x *= v.x;
        this.y *= v.y;
        this.z *= v.z;
        return this;
    },
    multiplyScalar: function(scalar) {
        this.x *= scalar;
        this.y *= scalar;
        this.z *= scalar;
        return this;
    },
    multiplyVectors: function(a, b) {
        this.x = a.x * b.x;
        this.y = a.y * b.y;
        this.z = a.z * b.z;
        return this;
    },
    applyEuler: function() {
        var quaternion;
        return function(euler) {
            if (euler instanceof Euler === false) {
                console.error('Vector3: .applyEuler() now expects a Euler rotation rather than a Vector3 and order.');
            }
            if (quaternion === undefined) quaternion = new Quaternion();
            this.applyQuaternion(quaternion.setFromEuler(euler));
            return this;
        };
    }(),
    applyAxisAngle: function() {
        var quaternion;
        return function(axis, angle) {
            if (quaternion === undefined) quaternion = new Quaternion();
            this.applyQuaternion(quaternion.setFromAxisAngle(axis, angle));
            return this;
        };
    }(),
    applyMatrix3: function(m) {
        var x = this.x;
        var y = this.y;
        var z = this.z;
        var e = m.elements;
        this.x = e[0] * x + e[3] * y + e[6] * z;
        this.y = e[1] * x + e[4] * y + e[7] * z;
        this.z = e[2] * x + e[5] * y + e[8] * z;
        return this;
    },
    applyMatrix4: function(m) {
        // input: Matrix4 affine matrix
        var x = this.x,
            y = this.y,
            z = this.z;
        var e = m.elements;
        this.x = e[0] * x + e[4] * y + e[8] * z + e[12];
        this.y = e[1] * x + e[5] * y + e[9] * z + e[13];
        this.z = e[2] * x + e[6] * y + e[10] * z + e[14];
        return this;
    },
    applyProjection: function(m) {
        // input: Matrix4 projection matrix
        var x = this.x,
            y = this.y,
            z = this.z;
        var e = m.elements;
        var d = 1 / (e[3] * x + e[7] * y + e[11] * z + e[15]); // perspective divide
        this.x = (e[0] * x + e[4] * y + e[8] * z + e[12]) * d;
        this.y = (e[1] * x + e[5] * y + e[9] * z + e[13]) * d;
        this.z = (e[2] * x + e[6] * y + e[10] * z + e[14]) * d;
        return this;
    },
    applyQuaternion: function(q) {
        var x = this.x;
        var y = this.y;
        var z = this.z;
        var qx = q.x;
        var qy = q.y;
        var qz = q.z;
        var qw = q.w;
        // calculate quat * vector
        var ix = qw * x + qy * z - qz * y;
        var iy = qw * y + qz * x - qx * z;
        var iz = qw * z + qx * y - qy * x;
        var iw = -qx * x - qy * y - qz * z;
        // calculate result * inverse quat
        this.x = ix * qw + iw * -qx + iy * -qz - iz * -qy;
        this.y = iy * qw + iw * -qy + iz * -qx - ix * -qz;
        this.z = iz * qw + iw * -qz + ix * -qy - iy * -qx;
        return this;
    },
    transformDirection: function(m) {
        // input: Matrix4 affine matrix
        // vector interpreted as a direction
        var x = this.x,
            y = this.y,
            z = this.z;
        var e = m.elements;
        this.x = e[0] * x + e[4] * y + e[8] * z;
        this.y = e[1] * x + e[5] * y + e[9] * z;
        this.z = e[2] * x + e[6] * y + e[10] * z;
        this.normalize();
        return this;
    },
    divide: function(v) {
        this.x /= v.x;
        this.y /= v.y;
        this.z /= v.z;
        return this;
    },
    divideScalar: function(scalar) {
        if (scalar !== 0) {
            var invScalar = 1 / scalar;
            this.x *= invScalar;
            this.y *= invScalar;
            this.z *= invScalar;
        } else {
            this.x = 0;
            this.y = 0;
            this.z = 0;
        }
        return this;
    },
    min: function(v) {
        if (this.x > v.x) {
            this.x = v.x;
        }
        if (this.y > v.y) {
            this.y = v.y;
        }
        if (this.z > v.z) {
            this.z = v.z;
        }
        return this;
    },
    max: function(v) {
        if (this.x < v.x) {
            this.x = v.x;
        }
        if (this.y < v.y) {
            this.y = v.y;
        }
        if (this.z < v.z) {
            this.z = v.z;
        }
        return this;
    },
    clamp: function(min, max) {
        // This function assumes min < max, if this assumption isn't true it will not operate correctly
        if (this.x < min.x) {
            this.x = min.x;
        } else if (this.x > max.x) {
            this.x = max.x;
        }
        if (this.y < min.y) {
            this.y = min.y;
        } else if (this.y > max.y) {
            this.y = max.y;
        }
        if (this.z < min.z) {
            this.z = min.z;
        } else if (this.z > max.z) {
            this.z = max.z;
        }
        return this;
    },
    clampScalar: (function() {
        var min, max;
        return function(minVal, maxVal) {
            if (min === undefined) {
                min = new Vector3();
                max = new Vector3();
            }
            min.set(minVal, minVal, minVal);
            max.set(maxVal, maxVal, maxVal);
            return this.clamp(min, max);
        };
    })(),
    floor: function() {
        this.x = Math.floor(this.x);
        this.y = Math.floor(this.y);
        this.z = Math.floor(this.z);
        return this;
    },
    ceil: function() {
        this.x = Math.ceil(this.x);
        this.y = Math.ceil(this.y);
        this.z = Math.ceil(this.z);
        return this;
    },
    round: function() {
        this.x = Math.round(this.x);
        this.y = Math.round(this.y);
        this.z = Math.round(this.z);
        return this;
    },
    roundToZero: function() {
        this.x = (this.x < 0) ? Math.ceil(this.x) : Math.floor(this.x);
        this.y = (this.y < 0) ? Math.ceil(this.y) : Math.floor(this.y);
        this.z = (this.z < 0) ? Math.ceil(this.z) : Math.floor(this.z);
        return this;
    },
    negate: function() {
        this.x = -this.x;
        this.y = -this.y;
        this.z = -this.z;
        return this;
    },
    dot: function(v) {
        return this.x * v.x + this.y * v.y + this.z * v.z;
    },
    lengthSq: function() {
        return this.x * this.x + this.y * this.y + this.z * this.z;
    },
    length: function() {
        return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
    },
    lengthManhattan: function() {
        return Math.abs(this.x) + Math.abs(this.y) + Math.abs(this.z);
    },
    normalize: function() {
        return this.divideScalar(this.length());
    },
    setLength: function(l) {
        var oldLength = this.length();
        if (oldLength !== 0 && l !== oldLength) {
            this.multiplyScalar(l / oldLength);
        }
        return this;
    },
    lerp: function(v, alpha) {
        this.x += (v.x - this.x) * alpha;
        this.y += (v.y - this.y) * alpha;
        this.z += (v.z - this.z) * alpha;
        return this;
    },
    cross: function(v, w) {
        if (w !== undefined) {
            console.warn('Vector3: .cross() now only accepts one argument. Use .crossVectors( a, b ) instead.');
            return this.crossVectors(v, w);
        }
        var x = this.x,
            y = this.y,
            z = this.z;
        this.x = y * v.z - z * v.y;
        this.y = z * v.x - x * v.z;
        this.z = x * v.y - y * v.x;
        return this;
    },
    crossVectors: function(a, b) {
        var ax = a.x,
            ay = a.y,
            az = a.z;
        var bx = b.x,
            by = b.y,
            bz = b.z;
        this.x = ay * bz - az * by;
        this.y = az * bx - ax * bz;
        this.z = ax * by - ay * bx;
        return this;
    },
    projectOnVector: function() {
        var v1, dot;
        return function(vector) {
            if (v1 === undefined) v1 = new Vector3();
            v1.copy(vector).normalize();
            dot = this.dot(v1);
            return this.copy(v1).multiplyScalar(dot);
        };
    }(),
    projectOnPlane: function() {
        var v1;
        return function(planeNormal) {
            if (v1 === undefined) v1 = new Vector3();
            v1.copy(this).projectOnVector(planeNormal);
            return this.sub(v1);
        }
    }(),
    reflect: function() {
        // reflect incident vector off plane orthogonal to normal
        // normal is assumed to have unit length
        var v1;
        return function(normal) {
            if (v1 === undefined) v1 = new Vector3();
            return this.sub(v1.copy(normal).multiplyScalar(2 * this.dot(normal)));
        }
    }(),
    angleTo: function(v) {
        var theta = this.dot(v) / (this.length() * v.length());
        // clamp, to handle numerical problems
        return Math.acos(Math.clamp(theta, -1, 1));
    },
    distanceTo: function(v) {
        return Math.sqrt(this.distanceToSquared(v));
    },
    distanceToSquared: function(v) {
        var dx = this.x - v.x;
        var dy = this.y - v.y;
        var dz = this.z - v.z;
        return dx * dx + dy * dy + dz * dz;
    },
    setEulerFromRotationMatrix: function(m, order) {
        console.error('Vector3: .setEulerFromRotationMatrix() has been removed. Use Euler.setFromRotationMatrix() instead.');
    },
    setEulerFromQuaternion: function(q, order) {
        console.error('Vector3: .setEulerFromQuaternion() has been removed. Use Euler.setFromQuaternion() instead.');
    },
    getPositionFromMatrix: function(m) {
        console.warn('Vector3: .getPositionFromMatrix() has been renamed to .setFromMatrixPosition().');
        return this.setFromMatrixPosition(m);
    },
    getScaleFromMatrix: function(m) {
        console.warn('Vector3: .getScaleFromMatrix() has been renamed to .setFromMatrixScale().');
        return this.setFromMatrixScale(m);
    },
    getColumnFromMatrix: function(index, matrix) {
        console.warn('Vector3: .getColumnFromMatrix() has been renamed to .setFromMatrixColumn().');
        return this.setFromMatrixColumn(index, matrix);
    },
    setFromMatrixPosition: function(m) {
        this.x = m.elements[12];
        this.y = m.elements[13];
        this.z = m.elements[14];
        return this;
    },
    setFromMatrixScale: function(m) {
        var sx = this.set(m.elements[0], m.elements[1], m.elements[2]).length();
        var sy = this.set(m.elements[4], m.elements[5], m.elements[6]).length();
        var sz = this.set(m.elements[8], m.elements[9], m.elements[10]).length();
        this.x = sx;
        this.y = sy;
        this.z = sz;
        return this;
    },
    setFromMatrixColumn: function(index, matrix) {
        var offset = index * 4;
        var me = matrix.elements;
        this.x = me[offset];
        this.y = me[offset + 1];
        this.z = me[offset + 2];
        return this;
    },
    equals: function(v) {
        return ((v.x === this.x) && (v.y === this.y) && (v.z === this.z));
    },
    fromArray: function(array) {
        this.x = array[0];
        this.y = array[1];
        this.z = array[2];
        return this;
    },
    toArray: function() {
        return [this.x, this.y, this.z];
    },
    clone: function() {
        return new Vector3(this.x, this.y, this.z);
    }
};
// --------------------------------------------------------do not edit or remove----------------------------------------------------------//
// --------------------------------------------------------END----------------------------------------------------------//
var first = false;
var second = false;
var third = false;
var fourth = false;
var cat4 = false;
var cat5 = false;
var fourth = false;
var onComplete = true;
var currneAnim;

var preLoadImage1 = new Image();
var preLoadImage2 = new Image();
var preLoadImage3 = new Image();

var preLoadImage4 = new Image();
var preLoadImage5 = new Image();
var preLoadImage6 = new Image();
var preLoadImage7 = new Image();
var preLoadImage8 = new Image();

function load_img(){
        preLoadImage1.src='images_gl/loaderblock.jpg';
        preLoadImage2.src='images_gl/loader_011.png';
        preLoadImage3.src='images_gl/loaderbar.png';
//        preLoadImage4.src='images_gl/Cloud_Controller/buttons/Cloud_7.svg';
//        preLoadImage5.src='images_gl/Cloud_Controller/buttons/Cloud_4.svg';
	   
      preLoadImage5.onload = afterLoad;
}
  
function afterLoad(){
    $('#transPatch').css('display','block');
    $('.fullScreenBox,#close_btn,#logoAdidas,#logoPredator').css('visibility','visible');
	  
}

 $(document).ready(function() {
             load_img(); 
     
     $(document).on('click', '.playAll', autoPlayAllAnimations)
     $(document).on('click', '.pauseAll', autoPauseAllAnimations)
});

$(window).load(function(){
     // load_img(); 
});

function closeSuperblaze(){
    scene.stop();
    $(window.parent).unbind('resize');
    window.top.document.getElementById("mainpanel2").contentWindow.stopAutoplay();
    autoplayCatalog=window.top.document.getElementById("mainpanel2").contentWindow.autoplayCatalog;
    $("#superblazeIframe",window.parent.document).css('display','none');
    window.top.document.getElementById("mainpanel2").contentWindow.superblazeClosed();
}

$(function(){
    resizePage(window.innerWidth,window.innerHeight);
    resizePage(window.document.documentElement.clientWidth,window.document.documentElement.clientHeight);
  if ((navigator.userAgent.indexOf('iPad') != -1) || (navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0)) {
     // console.log("ie1")
      $("#close").css('display', 'none');
            $("#fullScreen").css('display', 'none');
        } else {
            $("#fullScreen").css('display', 'block');
        }
    
//    if ((navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0)) {
//                           console.log("onlyie")
//                           $(".menuitems, .menuitems1").css("background-color","#4a4a4b");
//                                       $(".menuitems, .menuitems1").addClass("iespe");
//
//                           }
})
function closeOption(){
		for(i=1;i<=17;i++){
				$("#colors"+i).css("display","none");
				$("#forselectcolor"+i).css("display","none");
		}
		$("#colorTextforcat5").css("display","none");
}

$(window).load(function() {
				resizePage(window.document.documentElement.clientWidth,window.document.documentElement.clientHeight);    
				$(window).live('resize',function(){
                 resizePage(window.innerWidth,window.innerHeight);
        });
        window.onresize = function (event) {
             resizePage(window.innerWidth,window.innerHeight);
        }
       
});
  

function onReset() {
    onResetCameraClickGL(); //in _ui.js
}
	
function onZoomSlide(event, ui) {
    var val = -20 * (ui.value / 100) + 10;
    NavSetDolly(val);
    updateZoomBar(val);
    scene.clearRefine();
}
	
$(function() {
    // Slider
    //range: 'min',
    $('#zoom_slider').slider({
        orientation: "vertical",
        value: 155,
        min: 0,
        max: 205,
        slide: onZoomSlide
    });
    $('nodrag').on('dragstart', function(event) {
        event.preventDefault();
    });
    $('.nodrag').mousedown(function() {
        return false
    });

});

function buttonsZoom(value) {
    var delta = value;
    var deltaScene = (delta * 0.03) * (0.3);
    deltaScene = -deltaScene;
    if (NavSetDolly(g_navDolly + deltaScene)) {
        scene.clearRefine();
        updateZoomBar(g_navDolly-10);
    }
}
var updateEnabled = true;
var canvas = null,
    canvas2 = null;
var scene = null,
    scene2 = null;
var _scenePollInterval;
var outstandingJobs;
var totalJobs;
var firstTime = true;
var tempW = 5;
var animationLoading;
var autoplayAnim = false;


$(document).ready(function(){
    animationLoading = setInterval(function() {  
//                                 console.log("loaderbar>>")
                                tempW = tempW + 1;
                                if (tempW > 30) tempW = 30;
                                $("#loaderbar").css("width", tempW + "px"); 
                               
                            }, 100);
})
function isSuperblazeReady() {   
//    console.log("in")
     if (scene) {
                //totalJobs = 230;
                scene.start();
                outstandingJobs = scene.getOutstandingJobs();
//         console.log("outstandingJobs", outstandingJobs);
               if (!(scene._projectparsed /*&& scene._started*/)) {
                        if(firstTime){
                             
                            firstTime=false;
//                            animationLoading = setInterval(function() {  
//                                // console.log("loaderbar>>")
//                                tempW = tempW + 1;
//                                if (tempW > 30) tempW = 30;
//                                $("#loaderbar", window.parent.document).css("width", tempW + "px"); 
//                               
//                            }, 10);
                            
                        }
                } else if (outstandingJobs <= 0 && scene._prepared) {
                    onSuperBlazeReady();
                    clearInterval(_scenePollInterval);
                } else if (scene._projectparsed /*&& scene._started*/) {
                     clearInterval(animationLoading);
                     updateProgressBar();
                }
            }
	
}

function updateProgressBar() {
    totalJobs = scene.getTotalJobs();
    outstandingJobs = scene.getOutstandingJobs();
    var perc = 100 - Math.round(outstandingJobs / totalJobs * 100);
    // var newwidth = 170-(170 * (outstandingJobs / totalJobs))+20;
    var newwidth = 50 + 141*perc/100;
    if(newwidth<30) newwidth=30;
    //console.log("updateProgressBar -- loaderbar "+newwidth+"px perc "+perc+" jobs "+outstandingJobs+"/"+totalJobs);
    $("#loaderbar").css("width", newwidth + "px");
}
$( function() {
			$( "#accordion" ).accordion({
			heightStyle: "content",
			collapsible: true,
			speed: 'slow',
			active: false
			});
			$('#accordion h3#autoPlays').addClass('ui-state-disabled').off('click');
			$('#accordion h3#menu2').addClass('ui-state-disabled').off('click');
            $('#accordion h3#menu5').addClass('ui-state-disabled').off('click');
			$("#accordion h3#menu7").addClass( "ui-state-disabled" ).off('click');
            $('#accordion h3#menu9').addClass('ui-state-disabled').off('click');
			$("#accordion h3#menu10").addClass( "ui-state-disabled" ).off('click');
            $("#accordion h3#menu11").addClass( "ui-state-disabled" ).off('click');
            $("#accordion h3#menu12").addClass( "ui-state-disabled" ).off('click');
            $("#accordion h3#menu4").addClass( "ui-state-disabled" ).off('click');
            $("#accordion h3#menu6").addClass( "ui-state-disabled" ).off('click');
            $("#accordion h3#menu3").addClass( "ui-state-disabled" ).off('click');
            $("#accordion h3#menu8").addClass( "ui-state-disabled" ).off('click');
		});

		$(document).ready(function() {
			     
			});
			     var animStoped = true;
			     var animCntrlBlock = true;
			    $(window).load(function() {
			        var fc=true;
			         $(".menuitemsBase").click(function(){    
			             $("#panel").fadeToggle(200);
			                          autoPauseAllAnimations();
			         });
			
			         $(".menuitems").click(function(){  
//                          if (!animStoped || (!clickEventActive)) return;
                          if (!clickEventActive && !autoRotateState) return;
                       var newId = this.id; 
                       currneAnim = Number(newId.slice(4));
                if(prevAnimation==11 && currneAnim==11){
                    console.log("in_if_1111");
                 // objectHide();
                    for (var j = 1; j <= 10; j++) {translateOut(j);}
               }else{
                    console.log("in_else_1111");
                   for (var j = 1; j <= 11; j++) {
                       $('#point12text').css('display','none')
                       if(prevAnimation != currneAnim)
                       translateOut(j);
                   }
                    reversAll();
                       $("#point12text2").css("display","none");  
                       $("#point12text3").css("display","none");  
                       $("#point12text4").css("display","none");  
                   menu12Clicked=false;
                   
               }
				$("#rightAnim").css('display','block');
				scene.instanceSet("SR655", "visible", true);	
				scene.instanceSet("HDD_12", "visible", true);
				scene.instanceSet("Body_Ref", "visible", true);
				scene.instanceSet("three_five__", "visible", true);
				scene.clearRefine();		 
				pointShow();
              prevAnimation=currneAnim;
                        
//						$( "#accordion" ).accordion( "option", "disabled", true );  
                         $("#rightAnim").animate({right: '-235px'}, "slow");
                          rightAnimToggle = true;
                         autoRotateStop();
                         clearInterval(autoRotateInterval);
                         clearTimeout(autoPlayInt);                      
                         clearTimeout(myVar);                      
                         clearTimeout(startAutorot); 
                         $("#dummy-canvas").css("pointer-events","all");                       $("#rightAnim").css("display","block");  
			             firstAnim = true;
			             animblockStopped = false;			             
			              setTimeout(function(){
			                  animblockStopped = true;
			              },2000)
			              animStoped = false;   
                        for (var i=0; i<timeouts.length; i++) {
			                clearTimeout(timeouts[i]);
			             }
			              timeouts = [];

			              $(".menuitems").removeClass('active');
			                 
                         $(".menuitems").css("background-color","").css("opacity","");
					       
                         if(newId == "menu4"){
                            $(this).removeClass('active');
                             $(this).parents().prev(".menuitems").addClass('active');
                         }	

                         
                         $(this).addClass('active');
					      
			            
			             $(".noselect.pointcontent").removeClass("BlockClass");
			             
			              var a= "This is where the active feature text is shown -in a space saving place";
			              $("#point2text .descriptionDemo").html(a);
			              $("#point3text .descriptionDemo").html(a);
			              $("#point7text .descriptionDemo").html(a);
			              $("#point5text .descriptionDemo").html(a);
			             $(".greyOutBox").removeClass("disabled");
			             $(".animPlayBtns .greyOutBox, .greyOutBox").removeClass("redOutBox");
			             $("#cpSubHeading").text("");
			              if(autoplayAnim)autoPauseAllAnimations();
			              
                          console.log("currneAnim",currneAnim);
						  scene._nav._navMode = 0;
                         
			              console.log("id", newId, "currentAnimation", currneAnim);
								 	 switch (newId) {
                                        case "menu2":
                                        $("#accordion" ).accordion( "option", "active", false );
                                        menu2Click();
                                        break;
                                        case "menu3":
                                        menu3Click();
                                        $("#accordion" ).accordion( "option", "active", false );     
                                        break;
                                        case "menu4": 
                                        menu4Click();
                                        $( "#accordion" ).accordion( "option", "active",3 );     
                                        break;
                                        case "menu5":
                                        menu5Click();
                                        break;
                                        case "menu6":
                                        menu6Click();
                                        $( "#accordion" ).accordion( "option", "active",4);     
                                        break;
                                        case "menu7":
                                        menu7Click();
                                        break;
                                        case "menu8":
                                        menu8Click();
                                        $( "#accordion" ).accordion( "option", "active",5);     
                                        break;
                                        case "menu9": 
                                        menu9Click();
                                        break;
                                        case "menu10":
                                        $( "#accordion" ).accordion( "option", "active", false );
                                        menu10Click();
                                        break;
                                        case "menu11":
                                        $( "#accordion" ).accordion( "option", "active", false );
                                        menu12Click();
                                        break;
										case "menu13":
                                        menu13Click();
                                        break;
										case "menu14":
                                        menu14Click();
                                        break;
                                        
								 }
			         });
                    
     $(".point12click").click(function(){
         for (var i=0; i<timeouts.length; i++) {
                    clearTimeout(timeouts[i]);
         }
         timeouts = [];
         if(autoplayAnim)autoPauseAllAnimations();
         menu12Fadeout();
            $("#point12text2").fadeIn(500);
            $("#point12text3").fadeIn(500);
            $("#point12text4").fadeIn(500);
            $("#point12text7").fadeIn(500);
          var pointId = this.id; 
         console.log("pointId",pointId);
		 notrepeat = false;
         if(pointId == "point12text2"){
             point12anim1();
         }else if(pointId == "point12text3"){
             point12anim2();
         }else if(pointId == "point12text4"){
             point12anim3();
//         }else if(pointId == "point12text7"){
//             point12anim4();
         }
     });
                    
			     });



var firstAnim = true;
function fadingEffect (selector){
//    animStoped = false;
    firstAnim = false;
    var width = $("#"+selector).width();
    console.log("width", width);
for(i= 100 ; i> 0;i--){
 $("#"+selector).animate({width: i+"%"},0.5);
}
}
var set1_1;
var set1_2;
var set1_3;
var set1_4;
var set1_5;
var set1_6;
    
function clearSets(){
        clearTimeout(set1_1);
        clearTimeout(set1_2);
        clearTimeout(set1_3);
        clearTimeout(set1_4);
        clearTimeout(set1_5);
        clearTimeout(set1_6);

}


 function function11(callback) {
    console.log("1")
    $("#textFadeClass_01").css("display","block");
    fadingEffect("txtfadeEffetCls_01");
     set1_1 = setTimeout(function() {
        callback();
    }, 2500);
}

function function22(callback2) {
    console.log("2")
    $("#textFadeClass_02").css("display","block");
    fadingEffect("txtfadeEffetCls_02");
        set1_2 = setTimeout(function() {
        callback2();
    }, 2500);

}

function function33(callback3) {
    console.log("3")
     $("#textFadeClass_03").css("display","block");
    fadingEffect("txtfadeEffetCls_03");
	   set1_3 = setTimeout(function() {
        callback3();
    }, 2500);
}

function function44(callback4) {
    console.log("4")
     $("#textFadeClass_04").css("display","block");
    fadingEffect("txtfadeEffetCls_04");
       set1_4 = setTimeout(function() {
        callback4();
    }, 2500);

}
function function55() {
    console.log("5")
     $("#textFadeClass_05").css("display","block");
    fadingEffect("txtfadeEffetCls_05");
    set1_5 = setTimeout(function() {
//        animComplete();
        firstAnim = true;
//        $(".menuitems, .menuitems1").css('display', 'block');
    }, 2500);

}

function callbackChain(){
function11(function() {
    function22(function() {
        function33(function() {
            function44(function() {
                function55(); 
            }); 
        });
    });
});  
}




function menuFading(){
	$("#menu2").fadeIn(400, function(){
		$("#menu3").fadeIn(400, function(){
			$("#menu4").fadeIn(400, function(){
				$("#menu5").fadeIn(400, function(){
					$("#menu6").fadeIn(400, function(){
						$("#menu7").fadeIn(400, function(){
							$("#menu8").fadeIn(400, function(){
								$("#menu9").fadeIn(400, function(){
								    $("#menu10").fadeIn(400, function(){
                                          $("#menu11").fadeIn(400, function(){
											  $("#menu13").fadeIn(400, function(){
												$("#menu14").fadeIn(400, function(){
								             		$("#autoPlays").fadeIn(400);
												  })
											  })	  
                                         })
							        })
							     })
							})
						})
					})
				})
			})
		})	
	})
}

function onSuperBlazeReady() {    
				scene._jitRadius = 4;
				scene._zNearMin = 5.0;
				if(mob) scene._bDoF=false;
				window.addEventListener('focus', onWindowFocus, false);
				window.addEventListener('blur', onWindowBlur, false);
                
//                $("#IntroImageWrapper img").attr("src", "images_gl/Intro/Slide1.svg");
//     scene.gotoPosInTime(5.808148887699151,0.010828547132702444,-4.08192930709112,-1.084165557624836,38.70686868753819,1);
     scene.gotoPosInTime(0.06978706880240318,0.09081658792820413,-4.684769627099397,0.19013270528124104,63.34002041452978,1);
	
        end = new Date().getTime();
        var time = end - start;
        if(time<60000){
//            RT_RecordTiming("Load", time, "ThinkSystem DM Series Unified Hybrid Flash Storage");
        }
        console.log('End time: ' + time);
        
        setTimeout(function() {
						showScene();
						$("#reset").css("visibility", "visible");
						$("#transPatch2").css("display", "none");
						$("#loader,#loader1,#loader2,#transPatch").css("display", "none"); 
						$("#canvasContainer").css("visibility", "visible");
						$("#superblazeWrapper").css('display', 'block');
						$("#superblaze").css('display', 'block');
                        $("#pointtext1 div, #pointtext1 ul").css("display", "none");
            			$("#transPatch5").css('display', 'block');
                        $('#reset').css('visibility','visible');
                        $("#point3Div").css('display','none'); 
                        $("#point5Div").css('display','none');  
                        $("#transPatchDiv").css('display','none'); 
                        $("#point7Div").css('display','none');
                        $("#HeadingDiv").css('display','none');  
						
						rightAnimClick();
						timeouts.push(setTimeout(function(){
							$("#rightAnim").animate({right: '-235px'}, "slow");
        					rightAnimToggle = true;
						},5000));	
                        setTimeout(function(){
                            if(autoplayCatalog) {
                                autoPlayAllAnimations();
                            }
                        },8000);
						if ((navigator.userAgent.indexOf('iPad') != -1) || (navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0)) {
						//console.log("ie")
							$("#fullScreen").css('display', 'none');
                            $("#loader,#loader1,#loader2,#transPatch").css("display", "none"); 
						} else {
								$("#fullScreen").css('display', 'block');
						}
        }, 500);
    $(".menuitems, .menuitems1").css('display', 'none');
     UiLoader();
}

function imgPreLoader(){
    $.preloadImages = function() {
     for (var i = 0; i < arguments.length; i++) {
      $("<img />").attr("src", arguments[i]);
     }
    }

$.preloadImages("./images_gl/loaderblock.jpg",
"./images_gl/loader_011.png",
"./images_gl/loaderbar.png",
"./images_gl/loader.gif",
"./images_gl/intel.png",
"./images_gl/Play.svg",
"./images_gl/right_popup.svg",
"./images_gl/Lenovo.svg",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/0.png",
"./images_gl/lines/4.png",
"./images_gl/lines/0.png",
"./images_gl/lines/0.png",
"./images_gl/lines/0.png",
"./images_gl/lines/4.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/1.png",
"./images_gl/lines/2.png",
"./images_gl/lines/2.png",
"./images_gl/lines/0.png",
"./images_gl/lines/0.png",
"./images_gl/lines/0.png",
"./images_gl/lines/0.png",
"./images_gl/lines/3.png",
"./images_gl/intel.png",
"./images_gl/lines/5.png",
//"./images_gl/01.png",
//"./images_gl/02.png",
//"./images_gl/03.png",
				
"./images_gl/EPYC_Logo.png",
"./images_gl/model/model_1.png",
"./images_gl/model/model_5.png",
"./images_gl/model/model_3.png",
"./images_gl/model/model_4.png",
	
"../../superblaze_demo_images/reset.png",
"images_gl/Services/1.png",
"images_gl/Services/2.png",
"images_gl/Services/3.png",
"images_gl/Services/4.png",
"images_gl/Services/5.png",
"images_gl/Services/1_1.png",
"images_gl/Services/1_2.png",
"images_gl/Services/1_3.png",
"images_gl/Services/1_4.png"
               );
}

function UiLoader(){

    
    $("#hamb img").attr("src", "./images_gl/hamburger.png");
	$("#resetBtn img").attr("src", "./images_gl/reset.svg");
	$("#lenovo_logo img").attr("src", "./images_gl/Lenovo.svg");
//	$("#fullScreen img").attr("src", "../images_gl/Fullscreen_01.png");
    $("#rightAnim img").attr("src", "./images_gl/right_popup.svg"); 	
	$("#pauseplayImg img").attr("src", "./images_gl/Play.svg");
    
    $("#loader img").attr("src","./images_gl/loaderblock.jpg");
    $("#loader1 img").attr("src","./images_gl/loader_011.png");
    $("#loaderbar img").attr("src","./images_gl/loaderbar.png");
    $("#loaderDfr img").attr("src","./images_gl/loader.gif");
    $("#point1image2 img").attr("src","./images_gl/EPYC_Logo.png");
    $("#pauseplayImg img").attr("src","./images_gl/Play.svg");
    $("#rightAnim img").attr("src","./images_gl/right_popup.svg");
    $("#lenovo_logo img").attr("src","./images_gl/Lenovo.svg");
   
    $("#hotspot1plus.plus").attr("src","./images_gl/Drive/90X23.png");
    $("#hotspot2plus.plus").attr("src","./images_gl/Drive/2X110.png");
    $("#hotspot3plus.plus").attr("src","./images_gl/Drive/23X137.png");
    $("#hotspot4plus.plus").attr("src","./images_gl/Drive/23X137.png");    
    $("#hotspot5plus.plus").attr("src","./images_gl/PCIe/90X23.png");
    $("#hotspot6plus.plus").attr("src","./images_gl/PCIe/2X110.png");
    $("#hotspot7plus.plus").attr("src","./images_gl/PCIe/2X110.png");
    $("#hotspot8plus.plus").attr("src","./images_gl/PCIe/23X137.png");
    $("#hotspot9plus.plus").attr("src","./images_gl/PCIe/4-.png");
    $("#hotspot10plus.plus").attr("src","./images_gl/PCIe/23X119.png");
    $("#hotspot11plus.plus").attr("src","./images_gl/PCIe/35X106.png"); $("#hotspot111plus.plus").attr("src","./images_gl/PCIe/23X137.png"); 
    $("#hotspot12plus.plus").attr("src","./images_gl/NVMe/23_60.png");
    $("#hotspot13plus.plus").attr("src","./images_gl/NVMe/2X110.png");
    $("#hotspot14plus.plus").attr("src","./images_gl/NVMe/2X110.png");
    $("#hotspot15plus.plus").attr("src","./images_gl/NVMe/23_60.png");
    $("#hotspot16plus.plus").attr("src","./images_gl/NVMe/90X23.png");
	$("#hotspot114plus.plus").attr("src","./images_gl/NVMe/2X110.png");
	
	$("#point3img1 img").attr("src","./images_gl/model/model_1.png");
	$("#point3img2 img").attr("src","./images_gl/model/model_5.png");
	$("#point3img3 img").attr("src","./images_gl/model/model_3.png");
	$("#point3img4 img").attr("src","./images_gl/model/model_4.png");
	$(".point10textimg img").attr("src","./images_gl/EPYC_Logo.png");
	
	
	$("#hotspot17plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot18plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot19plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot20plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot21plus.plus").attr("src","./images_gl/lines/4.png");
	$("#hotspot22plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	
	$("#hotspot23plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot24plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot25plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot26plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot27plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot28plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot29plus.plus").attr("src","./images_gl/PCIe/120X16.png");
	$("#hotspot30plus.plus").attr("src","./images_gl/PCIe/120X16.png");
	$("#hotspot31plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot32plus.plus").attr("src","./images_gl/lines/4.png");
	$("#hotspot33plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	
	$("#hotspot34plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot35plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot36plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot37plus.plus").attr("src","./images_gl/PCIe/23X119.png");
	$("#hotspot38plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot39plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot40plus.plus").attr("src","./images_gl/PCIe/120X16.png");
	$("#hotspot41plus.plus").attr("src","./images_gl/PCIe/90X23.png");
	$("#hotspot42plus.plus").attr("src","./images_gl/lines/4.png");
	$("#hotspot43plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	
	$("#hotspot211plus.plus").attr("src","./images_gl/lines/4-1.png");
	$("#hotspot212plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot213plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot214plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot215plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot216plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot217plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	
	$("#hotspot311plus.plus").attr("src","./images_gl/lines/4-1.png");
	$("#hotspot312plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot313plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot314plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot315plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot316plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot317plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	
	$("#hotspot411plus.plus").attr("src","./images_gl/lines/4-1.png");
	$("#hotspot412plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot413plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot414plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot415plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	$("#hotspot416plus.plus").attr("src","./images_gl/NVMe/23_60.png");
	$("#hotspot417plus.plus").attr("src","./images_gl/PCIe/2X110.png");
	
   
    $("#point7image1 img").attr("src","./images_gl/intel.png");
//    $("#hotspot23plus.plus").attr("src","./images_gl/lines/5.png");
//    $("#point10image1 img").attr("src","./images_gl/01.png");
//    $("#pont10Img1 img").attr("src","./images_gl/02.png");
//    $("#pont10Img2 img").attr("src","./images_gl/03.png");
    
    $("#point12image1 img").attr("src","images_gl/Services/1.png");
    $("#point12image2 img").attr("src","images_gl/Services/2.png");
    $("#point12image3 img").attr("src","images_gl/Services/3.png");
    $("#point12image4 img").attr("src","images_gl/Services/4.png");
    $("#point12image5 img").attr("src","images_gl/Services/5.png");
    
    $("#point12image1_1 img").attr("src","images_gl/Services/1_1.png");
    $("#point12image1_2 img").attr("src","images_gl/Services/1_2.png");
    $("#point12image1_3 img").attr("src","images_gl/Services/1_3.png");
    $("#point12image1_4 img").attr("src","images_gl/Services/1_4.png");
 
    imgPreLoader();
	var img = new Image();
      img.onload = function(){
    }
}


$(document).ready(function(){
   try{
    parent.document;
        // accessible
        resizePage(window.parent.document.documentElement.clientWidth,window.parent.document.documentElement.clientHeight);
        if(window.parent.parent.bandwidth){     
        autoplayCatalog=window.top.document.getElementById("mainpanel2").contentWindow.autoplayCatalog;
        ////console.log("content window"+autoplayCatalog);
        }else{
            autoplayCatalog=false;
            $("#home").css("display","none");
            $("#backText").css("display","none");

        }
       $(window.parent).bind('resize',function(){
                 resizePage(window.parent.innerWidth,window.parent.innerHeight);
        });
       window.onresize = function (event) {
             resizePage(window.parent.innerWidth,window.parent.innerHeight);
        }
        $(window).bind("fullscreen-toggle", function(e, state) {
            ////console.log("full toggle");
            resizePage(window.parent.document.documentElement.clientWidth,window.parent.document.documentElement.clientHeight);
        });
    }catch(e){
        // not accessible
        resizePage(window.document.documentElement.clientWidth,window.document.documentElement.clientHeight);
        autoplayCatalog=false;
        $("#home").css("display","none");
        $("#backText").css("display","none");
        $(window).bind('resize',function(){
                 resizePage(window.innerWidth,window.innerHeight);
        });
        window.onresize = function (event) {
             resizePage(window.innerWidth,window.innerHeight);
        }
        $(window).bind("fullscreen-toggle", function(e, state) {
            ////console.log("full toggle");
            resizePage(window.document.documentElement.clientWidth,window.document.documentElement.clientHeight);
        });
    } 
});



function SuperblazeStart(gl) {
    try {
        parent.document;
        resizePage(document.documentElement.clientWidth, document.documentElement.clientHeight);
        $(window).resize(function() {
            resizePage(document.documentElement.clientWidth, document.documentElement.clientHeight);

        });
       
    } catch (e) {
        resizePage(document.documentElement.clientWidth, document.documentElement.clientHeight);
        $(window).resize(function() {
            resizePage(document.documentElement.clientWidth, document.documentElement.clientHeight);

        });
        
    }
    canvas = document.getElementById("superblaze-canvas");
    var is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;

    if ((navigator.userAgent.indexOf("iPhone") != -1) || ((navigator.userAgent.indexOf("Android") != -1) || (navigator.userAgent.indexOf("Mobile") != -1)) || (navigator.userAgent.indexOf('iPod') != -1)) {
        
//        scene = new infinityrt_scene(gl, "../v5/model_gl/", canvas.width, canvas.height);
        scene = new infinityrt_scene(gl, "model_gl/", canvas.width, canvas.height);
        //console.log("mob");
    } else {

//        scene = new infinityrt_scene(gl, "../v5/model_gl/", canvas.width, canvas.height);
        scene = new infinityrt_scene(gl, "model_gl/", canvas.width, canvas.height);
        
        //console.log("desk");
    }
     scene.fnLoadProgress = updateProgressBar;
    scene.start();
    scene._nav = new infinityrt_navigation(scene, canvas.width, canvas.height);
    _scenePollInterval = setInterval(isSuperblazeReady, 100);
     start = new Date().getTime();
//    NavInit(canvas.width, canvas.height);
    var canvasDummy = document.getElementById("dummy-canvas");
    addMouseListeners(canvasDummy);
   /* scene._slowinoutfac = 0.9;*/
    if (scene != null) {

    
        window.requestAnimationFrame(frameUpdate);
        $(this).bind("contextmenu", onRightClick); //prevents a right click     
        document.body.oncontextmenu = onRightClick;
        //window.addEventListener('oncontextmenu',onRightClick,false);
        //if (typeof(onInit()) != 'undefined') onInit();
    }
    initDragCursor();
}
var mob = (navigator.userAgent.indexOf("iPhone") != -1) || ((navigator.userAgent.indexOf("Android") != -1) || (navigator.userAgent.indexOf("Mobile") != -1)) || (navigator.userAgent.indexOf('iPod') != -1);

var FullscreenOff = false;

function launchFullscreen(element) {
//    window.parent.fullScreen=true;
//    resizePage(window.parent.document.documentElement.clientWidth,window.parent.document.documentElement.clientHeight);
//    if(navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0){
//        //console.log("IE 11");
//        $("#fullScreenOff").css('display','none'); 
//        $("#fullScreen").css('display','none');
//        
//    }else{
//      //  console.log("Not IE 11");
//        $("#fullScreenOff").css('display','block'); 
//        $("#fullScreen").css('display','none');
//    }
//    
//   // console.log(" full screen ");
//    if(element.requestFullscreen) {
//        element.requestFullscreen();
//    } else if(element.mozRequestFullScreen) {
//        element.mozRequestFullScreen();
//    } else if(element.webkitRequestFullscreen) {
//        element.webkitRequestFullscreen();
//    } else if(element.msRequestFullscreen) {
//        element.msRequestFullscreen();
//    }
       //setTimeout(function(){resizePage(window.parent.document.documentElement.clientWidth,window.parent.document.documentElement.clientHeight);;}, 2000);
}

function exitFullscreen() { 
   // console.log("Exit full screen");
//    window.parent.fullScreen=false;
//    $("#fullScreenOff").css('display','none'); 
//    $("#fullScreen").css('display','block');  
//    if (window.parent.document.exitFullscreen) {
//        window.parent.document.exitFullscreen();
//    } else if (window.parent.document.mozCancelFullScreen) {
//        window.parent.document.mozCancelFullScreen();
//    } else if (window.parent.document.webkitExitFullscreen) {
//        window.parent.document.webkitExitFullscreen();
//    }
//    setTimeout(function() {
//        resizePage(window.parent.document.documentElement.clientWidth, window.parent.document.documentElement.clientHeight);
//    }, 40);

}

window.document.onkeyup = function (e){
   // console.log("ECS pressed IE1");
    if (e.keyCode == 27) { // escape key maps to keycode `27`
        // if(navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0){
        //    // console.log("ECS pressed IE");
        // }
       // console.log("ECS pressed"); 
        // exitFullscreen(window.parent.document.documentElement);
        var iE = 0;
        var _intervalEsc = setInterval(function () {
            if(iE < 5){
               // console.log("func"+iE);
//                exitFullscreen(window.parent.document.documentElement);
                iE++;
            }else{
                clearInterval(_intervalEsc);
            }
        }, 10);
    }
}

var FullscreenOn = false;

function resizePage(width, height) { 
    // console.log("resize")
// alert("Resize page width: "+width+" height: "+height);
    if((navigator.userAgent.indexOf('iPad') != -1)){
        
        width=document.documentElement.clientWidth;
        height=document.documentElement.clientHeight;
       
    }
    
    if(mob){
            $("#fullScreen").css('display','none');
        }else if(navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0){
         // console.log("IE 11");
          $("#fullScreenOff").css('display','none'); 
          $("#fullScreen").css('display','none');
        }else{
            $("#fullScreenOff").css('display','none'); 
            $("#fullScreen").css('display','none');
        }
    
//    
       
//      FullscreenOn=window.parent.fullScreen;
      //// console.log(" resize page flscreen "+width+" "+height);
        if(mob){
        jQuery("#dummy-canvas").detach().appendTo('#maincanvasContainer');
        jQuery("#superblaze-canvas").detach().appendTo('#canvasContainer');
        $("#superblaze-canvas").attr({
            width: '1024px',
            height: '576px'
        });
    }
    var s;
    if(FullscreenOn == true){
        if(navigator.userAgent.indexOf('MSIE')!==-1 || navigator.appVersion.indexOf('Trident/') > 0){
           // console.log("IE 11 FS on");
            $("#fullScreenOff").css('display','none'); 
            $("#fullScreen").css('display','none');
        }else{
           // console.log("Not IE 11");
            $("#fullScreenOff").css('display','block'); 
            $("#fullScreen").css('display','none');
        }
        // $("#fullScreenOff").css('display','block');
         // $("#fullScreen").css('display','none'); 
        if (width > 1920) {
            width = 1920;
        }
        if (height > 1080) {
            height = 1080;
        }        
       
    }else{
        if(mob){
            $("#fullScreen").css('display','none');
        }else{
            
         $("#fullScreen").css('display','block');
         $("#fullScreenOff").css('display','none');
        } 

        if (width > 1920) {
            width = 1920;
        }
        if (height > 1080) {
            height = 1080;
        }
    }

    var w = eval(width / 1286);
    var h = eval(height / 723);

    if (w < h || (navigator.userAgent.indexOf('iPad') != -1)) {
       // console.log("Resize page2 width: "+width+" height: "+height);
         //// console.log(" width ...");
        s = w;
        sceneDivW=width;
        sceneDivH=1080*width/1920;
        //if(s<0.815 || mob){
            $("#scenediv").css({'width':"1284px",'height':"721px"});
            $("#dummy-canvas").css({'width':"1284px",'height':"721px"});
        /*}else{
            $("#scenediv").css({'width':sceneDivW,'height':sceneDivH});
            $("#dummy-canvas").css({'width':sceneDivW,'height':sceneDivH});
        }*/
        var div = document.getElementById("superblaze-canvas");
        if (div.getBoundingClientRect) {
            var rect = div.getBoundingClientRect();
            new_w = rect.right - rect.left;
            new_h = rect.bottom - rect.top;
        }
        if((navigator.userAgent.indexOf('iPad') != -1)){
           // console.log("resizing ipad....."+mob);
            $('#superblaze').css({
                'margin-left': 0,
                'margin-top': 0
            });
            $("#superblazeWrapper").css({
                'margin-left': 0,
                'margin-top':0
            });
            $('#canvasContainer').css({
                'margin-left': 0,
                'margin-top': 0
            });  
//            $("#menubar").removeClass("menuitems");
                        $("menuitems").hover(function(){
                    $(this).css("background-color", "yellow");
                    });
        }else if(mob){
           // console.log("resizing mob....."+mob);
            $('#superblaze').css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': 0
            });
            $("#superblazeWrapper").css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': 0
            });
            $('#canvasContainer').css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': 0
             });
        }else{
           // console.log("resizing else....."+mob);
            $('#superblaze').css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': parseInt(window.innerHeight - new_h) / 2
            });
            $("#superblazeWrapper").css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': parseInt(window.innerHeight - new_h) / 2
            });
            $('#canvasContainer').css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': parseInt(window.innerHeight - new_h) / 2
            });
        }
        
    } else {
       // console.log("height 22...");
        s = h;
		sceneDivH=height;
		sceneDivW=1920*height/1080;
		// if(s < 0.815 || mob){
            $("#scenediv").css({'width':"1284px",'height':"721px"});
            $("#dummy-canvas").css({'width':"1284px",'height':"721px"});
       /* }else{
            $("#scenediv").css({'width':sceneDivW,'height':sceneDivH});
            $("#dummy-canvas").css({'width':sceneDivW,'height':sceneDivH});
        }*/
		
        var div = document.getElementById("superblaze-canvas");
        if (div.getBoundingClientRect) {
            var rect = div.getBoundingClientRect();
            new_w = rect.right - rect.left;
            new_h = rect.bottom - rect.top;
        }
        if((navigator.userAgent.indexOf('iPad') != -1)){
           // console.log("resizing mob2....."+mob);
            $('#superblaze').css({
                'margin-left': 0,
                'margin-top': 0
            });
            $("#superblazeWrapper").css({
                'margin-left': 0,
                'margin-top':0
            });
            $('#canvasContainer').css({
                'margin-left': 0,
                'margin-top': 0
            });
        }else{
           // console.log("resizing else2....."+mob);
            $('#superblaze').css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': parseInt(window.innerHeight - new_h) / 2
            });
            $("#superblazeWrapper").css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': parseInt(window.innerHeight - new_h) / 2
            });
            $('#canvasContainer').css({
                'margin-left': (($(window).width() - new_w) / 2),
                'margin-top': parseInt(window.innerHeight - new_h) / 2
            });
        }
    }

       if(mob){
            $("#close").css("display","none");
            $("#fullScreen").css('display','none');
        }else{
            $("#zoomSliderContainer").css("display","block");
        }

        //// console.log("else ...");
        $("#superblaze").css({
            'transform': 'scale(' + s + ')',
            'transform-origin': '0% 0%',
            '-webkit-transform': 'scale(' + s + ')',
            '-webkit-transform-origin': '0% 0%',
            '-moz-transform': 'scale(' + s + ')',
            '-moz-transform-origin': '0% 0%',
            '-o-transform': 'scale(' + s + ')',
            '-o-transform-origin': '0% 0%',
            '-ms-transform': 'scale(' + s + ')',
            '-ms-transform-origin': '0% 0%',
        });
        $("#superblazeWrapper").css({
            'transform': 'scale(' + s + ')',
            'transform-origin': '0% 0%',
            '-webkit-transform': 'scale(' + s + ')',
            '-webkit-transform-origin': '0% 0%',
            '-moz-transform': 'scale(' + s + ')',
            '-moz-transform-origin': '0% 0%',
            '-o-transform': 'scale(' + s + ')',
            '-o-transform-origin': '0% 0%',
            '-ms-transform': 'scale(' + s + ')',
            '-ms-transform-origin': '0% 0%',
        });
   
    var ccs = s / 1.493001;
    if (mob) {
        ccs = s/0.79626;
    }
    $("#canvasContainer").css({
        'transform': 'scale(' + ccs + ')',
        'transform-origin': '0% 0%',

        '-webkit-transform': 'scale(' + ccs + ')',
        '-webkit-transform-origin': '0% 0%',

        '-moz-transform': 'scale(' + ccs + ')',
        '-moz-transform-origin': '0% 0%',

        '-o-transform': 'scale(' + ccs + ')',
        '-o-transform-origin': '0% 0%',

        '-ms-transform': 'scale(' + ccs + ')',
        '-ms-transform-origin': '0% 0%',
    });
}


function addMouseListeners(canvas) {
    canvas.addEventListener('mousemove', mouseMove, false);
    canvas.addEventListener('mousedown', mouseDown, false);
    canvas.addEventListener('mouseup', mouseUp, false);
    canvas.addEventListener('mousewheel', mouseWheel, false);
    canvas.addEventListener('DOMMouseScroll', mouseWheel, false);
    canvas.addEventListener('mouseout', mouseOut, false);
    canvas.addEventListener('touchstart', touchStart, false);
    canvas.addEventListener('touchmove', touchMove, false);
    canvas.addEventListener('touchend', touchEndCan, false);
//    document.getElementById('rightAnim').addEventListener('mousedown', rightAnimClick, false);
	document.getElementById("home").addEventListener("mousedown", closeSuperblaze);    
}


var rightAnimToggle = true;
var animblockStopped = true;   
var timeoutsnew = [];
var timeouts =[];
/*abhijitend*/

function rightAnimClick(){
	reversAll();
  if(rightAnimToggle){
			$("#rightAnim").animate({right: '0px'}, "slow");
			rightAnimToggle = false;
	}else{
			$("#rightAnim").animate({right: '-235px'}, "slow");
			rightAnimToggle = true;
	}
}

function pointShow(){
	$('#point5list').css("display","block");
	$('#point7list').css("display","block");
	$('#point9list').css("display","block");
}
function mouseDownHide(){
    $('.point9text1,.point9text2').css("opacity",0);
    $('#point3text').css("display","none");
    $('#point10text').css("display","none");
	$('#point5list').css("display","none");
	$('#point7list').css("display","none");
	$('#point9list').css("display","none");
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
}
function mouseWheelHide(){
    $('#point4text').css("display","none");
	$('#point5text').css("display","none");
    $('#point6text').css("display","none");
    $('#point7text').css("display","none");
    $('#point8text').css("display","none");
    $('#point9text').css("display","none");
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
}
function objectHide() {
         topCover = false;
         scene.animPlayInTime("top_panel", 0, 500);
         scene.animPlayInTime("HDD_CAGE", 0, 1);
         scene.animPlayInTime("HDD_Handle", 0, 1);
         scene.animPlayInTime("HDD_CAGE_SR655", 0, 1);
         scene.animPlayInTime("group156", 0, 1);
         scene.instanceSet("three_five_inchinterior_back", "visible", false);
         scene.instanceSet("PCI_bacck", "visible", false);
         scene.instanceSet("hdd_12", "visible", false);
         scene.instanceSet("NVME_back_01", "visible", false);
         scene.instanceSet("HDD_2_5_", "visible", false);
         scene.clearRefine();
	     setTimeout(function(){
		   clickEventActive = true;
	     },100);
}

var open=false;
var close=false;

function menu2Click(){
    console.log("menu2Clicked");
    $("#cpHeading").text("ThinkSystem SR655");
    objectHide();
    topCover=true;
    animStoped=false;
    $("#onloadCopy").css('display','block');
	$("#point13text").css('display','none');  
	$("#point14text").css('display','none');  
    $("#transparentPatch").css('display','none');
	scene.instanceSet("hdd_12", "visible", true);
	scene.instanceSet("three_five_inchinterior_back", "visible", true);
	scene.instanceSet("PCI_bacck", "visible", false);
	scene.instanceSet("NVME_back_01", "visible", false);
	scene.clearRefine();
    timeouts.push(setTimeout(function(){
scene.gotoPosInTime(0.06978706880240318,0.09081658792820413,-4.684769627099397,0.19013270528124104,63.34002041452978,1000);
    }, 400));
    startAutorot = timeouts.push(setTimeout(function(){
            autoRotateCall();
        console.log("autoRotateCall");
    }, 5000));
        
    timeouts.push(setTimeout(function(){
            $("#onloadCopy").fadeIn(400);
			
            timeouts.push(setTimeout(function(){
                translateIn(2);
                animComplete();
            }, 200));     
        
         if(autoplayAnim){
                animCompeteAuto();
            }

        $("#onloadCopy").css({
                "webkitTransform":"translate(0,-5px)",
                "MozTransform":"translate(0,-5px)",
                "msTransform":"translate(0,-5px)",
                "OTransform":"translate(0,-5px)",
                "transform":"translate(0,-5px)",
                "opacity":1
           });
       
    }, 2050));
	
scene.clearRefine();
}


function menu3Click(){
	scene._nav._navMode = 0;
    console.log("menu3_click_1");
    animStoped=false;
    
	$("#cpHeading").text(" ");
    animComplete();  
    objectHide();
	$("#point13text").css('display','none');  
	$("#point14text").css('display','none');  
	scene.instanceSet("hdd_12", "visible", true);
	scene.instanceSet("three_five_inchinterior_back", "visible", true);
	scene.instanceSet("PCI_bacck", "visible", false);
	scene.instanceSet("NVME_back_01", "visible", false);
	scene.instanceSet("HDD_12", "visible", false);
	scene.instanceSet("Body_Ref", "visible", false);
	scene.instanceSet("three_five__", "visible", false);
	scene.clearRefine();
   timeouts.push(setTimeout(function(){ scene.gotoPosInTime(6.18344441598199,0.025925687928204162,0.4810320681179014,-8.704350182421182,63.34002041452978,1000, function(){
	
   });
	}, 100));
	 		timeouts.push(setTimeout(function(){
               $("#point3text").css("display", "block"); 
            }, 1500));
	
	
				
        if(autoplayAnim){

                animCompeteAuto();
        }
    
  scene.clearRefine();	
}

var topCover=false;

function menu4Click(){
  console.log("menu4Clicked");
    animStoped=false;
    $("#cpHeading").html("Maximum 3.5&quot; drive configuration: 20x 3.5&quot; 12(F)+4(M)+4(R)"); 
	$("#onloadCopy").css('display','none');
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
	      
if(!topCover){
        console.log("if...")
        
        objectHide();
      	scene.instanceSet("hdd_12", "visible", true);
		scene.instanceSet("three_five_inchinterior_back", "visible", true);
		scene.instanceSet("PCI_bacck", "visible", false);
		scene.instanceSet("NVME_back_01", "visible", false);
		scene.clearRefine();
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(1.4682140040607652,1.5079644737231006,-4.80601296937878,2.194984328536714,111.61723332986423,800);
          
        }, 300)); 
        
       timeouts.push(setTimeout(function(){
            scene.animPlayInTime("top_panel", 1, 1000);
            scene.clearRefine(); 
		    }, 1100)); 
        timeouts.push(setTimeout(function(){
			scene.instanceSet("top_panel", "visible", false);
//            scene.animPlayInTime("HDD_CAGE", 1, 1000);
//            scene.animPlayInTime("HDD_Handle", 1, 1000);           
        }, 2100));  
        
        timeouts.push(setTimeout(function(){
            topCover = true;
            $("#point4text").fadeIn(400);
             
        }, 3100));  
        
                
      timeouts.push(setTimeout(function(){
               
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 4100));  
        
    }else{
		objectHide();
        console.log("else...")
        topCover = true;
        scene.instanceSet("top_panel", "visible", false); 
//        scene.animPlayInTime("HDD_CAGE", 1, 10);
//        scene.animPlayInTime("HDD_Handle", 1, 10);
		scene.instanceSet("hdd_12", "visible", true);
		scene.instanceSet("PCI_bacck", "visible", false);
		scene.instanceSet("NVME_back_01", "visible", false);
		scene.instanceSet("three_five_inchinterior_back", "visible", true);
        scene.clearRefine();
        
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(1.4682140040607652,1.5079644737231006,-4.80601296937878,2.194984328536714,111.61723332986423,800);
          
        }, 300)); 
		
		 timeouts.push(setTimeout(function(){
//            scene.animPlayInTime("HDD_CAGE", 1, 1000);
//            scene.animPlayInTime("HDD_Handle", 1, 1000);           
        }, 1100)); 
        
          timeouts.push(setTimeout(function(){
               $("#point4text").fadeIn(400);
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 2100));  
    }

  scene.clearRefine();  
}



function menu5Click(){
    console.log("menu5_click");
    $("#onloadCopy").css('display','none');
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
    $("#cpHeading").html("Maximum 3.5&quot; drive configuration: 20x 3.5&quot; 12(F)+4(M)+4(R)");
    $("#menu5").removeClass("disabled");
    $("#menu5").removeClass('active');
    $(".greyOutBox").removeClass('redOutBox');
    $("#menu5 .greyOutBox").addClass('redOutBox');
    objectHide();
	scene.instanceSet("hdd_12", "visible", true);
	scene.instanceSet("PCI_bacck", "visible", false);
	scene.instanceSet("NVME_back_01", "visible", false);
	scene.instanceSet("three_five_inchinterior_back", "visible", true);
	scene.clearRefine();
	
	timeouts.push(setTimeout(function(){ scene.gotoPosInTime(3.0108300535245873,-0.01855573747692496,-3.9211001201010096,-2.109821904136366,48.67427495331798,1500);
      }, 500));
	
   timeouts.push(setTimeout(function(){
		  $("#point5text").css('display','block');
		 	translateIn(5);
		 animComplete();
	}, 1500));
	
 timeouts.push(setTimeout(function(){
	 if(autoplayAnim){
                animCompeteAuto();
    }
  }, 2000));  
}


function menu6Click(){
    console.log("menu6Clicked");
     $("#onloadCopy").css('display','none');
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
     animStoped = false;
     menu6clicked = true;
    $("#cpHeading").text(" ");
      
    if(!topCover){
        console.log("if...")
        
       
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(1.4682140040607652,1.5079644737231006,-4.805872272378781,2.161136147319221,111.61723332986423,800);
          
        }, 300)); 
		timeouts.push(setTimeout(function(){ 
			 objectHide();
			scene.instanceSet("hdd_12", "visible", true);
			scene.clearRefine();
			scene.instanceSet("three_five_inchinterior_back", "visible", false);
			scene.instanceSet("PCI_bacck", "visible", true);
			scene.clearRefine();
        }, 600)); 
        
        timeouts.push(setTimeout(function(){
            scene.animPlayInTime("top_panel", 1, 1000);
        }, 1100));  
        
        timeouts.push(setTimeout(function(){
            topCover = true;
            $("#point6text").fadeIn(400);
            scene.instanceSet("top_panel", "visible", false);
            scene.instanceSet("three_five_inchinterior_back", "visible", false);
            scene.instanceSet("PCI_bacck", "visible", true);
            scene.clearRefine();  
        }, 2100));  
        
                
      timeouts.push(setTimeout(function(){
               
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 2100));  
        
    }else{
		objectHide();
        console.log("else...")
        topCover = true;
        scene.instanceSet("top_panel", "visible", false); 
        scene.instanceSet("three_five_inchinterior_back", "visible", false);
        scene.instanceSet("PCI_bacck", "visible", true);
		scene.instanceSet("hdd_12", "visible", true);
        scene.clearRefine();
        
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(1.4682140040607652,1.5079644737231006,-4.805872272378781,2.161136147319221,111.61723332986423,800);
          
        }, 300)); 
        
          timeouts.push(setTimeout(function(){
               $("#point6text").fadeIn(400);
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 1100));  
    }

  scene.clearRefine();    
    
}

function menu7Click() {
	console.log("menu7_click");
    objectHide();
    $("#menu7").removeClass("disabled");
    $("#menu7").removeClass('active');
     $(".greyOutBox").removeClass('redOutBox');
    $("#menu7 .greyOutBox").addClass('redOutBox');
    $("#cpHeading").html(" ");
    $("#onloadCopy").css('display','none');
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
	scene.instanceSet("three_five_inchinterior_back", "visible", false);
	scene.instanceSet("hdd_12", "visible", true);
	scene.instanceSet("NVME_back_01", "visible", false);
	scene.instanceSet("PCI_bacck", "visible", true);
	scene.clearRefine();
	
      timeouts.push(setTimeout(function(){ scene.gotoPosInTime(3.0108300535245873,-0.01855573747692496,-3.9211001201010096,-2.109821904136366,48.67427495331798, 1500);
      }, 500));
	
    timeouts.push(setTimeout(function(){
        $("#point7text").css('display','block');
		translateIn(7);
    }, 1500));
         
    timeouts.push(setTimeout(function(){ 
        if(autoplayAnim){
            animCompeteAuto();
        }else{
             animComplete(); 
        }
    }, 2000));
     
 }
    
function menu8Click() {
     animStoped = false;
     console.log("menu_8_clicked");
     $("#cpHeading").html("Storage-Rich Configuration");
     $("#onloadCopy").css("opacity","0").fadeOut(400);
	 $("#point13text").css('display','none');
	 $("#point14text").css('display','none');
    
    if(!topCover){
        console.log("if...")
        
		
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(1.4682140040607652,1.5079644737231006,-4.805872272378781,2.161136147319221,111.61723332986423,800);
          
        }, 300)); 
        timeouts.push(setTimeout(function(){
			scene.instanceSet("HDD_CAGE_SR655", "visible", true);
			objectHide();
			scene.instanceSet("HDD_2_5_", "visible", true);
			scene.clearRefine();
        }, 600));
        timeouts.push(setTimeout(function(){
            scene.animPlayInTime("top_panel", 1, 1000);
            scene.clearRefine(); 
        }, 1100)); 
		
		timeouts.push(setTimeout(function(){
			scene.instanceSet("top_panel", "visible", false);
//            scene.animPlayInTime("HDD_CAGE_SR655", 1, 1000);
			scene.clearRefine();
            $("#point8text").fadeIn(400);
        }, 2100));  
        
        timeouts.push(setTimeout(function(){
            topCover = true;
            scene.instanceSet("PCI_bacck", "visible", false);
            scene.instanceSet("hdd_12", "visible", false);
            scene.instanceSet("NVME_back_01", "visible", true);
            scene.instanceSet("HDD_2_5_", "visible", true);
            scene.clearRefine();  
        }, 1500));  
        
                
      timeouts.push(setTimeout(function(){
               
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 4100));  
        
    }else{
		objectHide();
        console.log("else...")
        topCover = true;
        scene.instanceSet("top_panel", "visible", false);
        scene.instanceSet("hdd_12", "visible", false);
        scene.instanceSet("HDD_2_5_", "visible", true);
		scene.instanceSet("three_five_inchinterior_back", "visible", false);
		scene.instanceSet("PCI_bacck", "visible", false);
		scene.instanceSet("NVME_back_01", "visible", true);
        scene.clearRefine();
        
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(1.4682140040607652,1.5079644737231006,-4.805872272378781,2.161136147319221,111.61723332986423,800);
          
        }, 300)); 
         
		timeouts.push(setTimeout(function(){ 
//			scene.animPlayInTime("HDD_CAGE_SR655", 1, 1000);
			scene.clearRefine();
		}, 1100)); 
		
          timeouts.push(setTimeout(function(){
               $("#point8text").fadeIn(400);
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 2100));  
    }

  scene.clearRefine();
}

var storage_dfr=false;
var menu9Clicked = false;
function menu9Click() {
    console.log("menu9Clicked");
    $("#onloadCopy").css("opacity","0").fadeOut(400);
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
    animStoped = false;
    objectHide();
    $("#cpHeading").text(" ");
     $("#menu9").removeClass("disabled");
    $("#menu9").removeClass('active');
     $(".greyOutBox").removeClass('redOutBox');
    $("#menu9 .greyOutBox").addClass('redOutBox');
    scene.instanceSet("PCI_bacck", "visible", false);
	scene.instanceSet("hdd_12", "visible", false);
	scene.instanceSet("NVME_back_01", "visible", true);
	scene.instanceSet("HDD_2_5_", "visible", true);
	scene.clearRefine();
         timeouts.push(setTimeout(function(){ scene.gotoPosInTime(3.0108300535245873,-0.01855573747692496,-3.9211001201010096,-2.109821904136366,48.67427495331798,1500);
         }, 500));
         timeouts.push(setTimeout(function(){
             $("#point9text").css('display','block');
                    translateIn(9);
            if(autoplayAnim){
                animCompeteAuto();
            }else{
                animComplete();
            }      
          }, 2000));
         
     }

function menu10Click() {
    console.log("menu10Clicked");   
    animStoped = false;
    $("#onloadCopy").css("display", "none"); 
	$("#point13text").css('display','none');
	$("#point14text").css('display','none');
    $("#cpHeading").text(" ");
    
    if(!topCover){
        console.log("10if");
        objectHide();
      	scene.instanceSet("hdd_12", "visible", true); 
		scene.instanceSet("top_panel", "visible", false);
		scene.instanceSet("three_five_inchinterior_back", "visible", false);
		scene.instanceSet("PCI_bacck", "visible", true); 
 		scene.clearRefine();
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(6.180231072275836,1.5079644737231006,-24.696843982475066,0.866810920613501,32.0655782039611,800);
          
        }, 500)); 
        
        
        timeouts.push(setTimeout(function(){
            scene.animPlayInTime("top_panel", 1, 1000);
        }, 1100));  
        
        timeouts.push(setTimeout(function(){
            topCover = true;
            $("#point10text").fadeIn(400);
            scene.instanceSet("top_panel", "visible", false);
            scene.clearRefine();  
        }, 2100));  
        
                
      timeouts.push(setTimeout(function(){
               
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 2100));  
        
    }else{
		console.log("10else");
        topCover = true;
		 objectHide();
		scene.instanceSet("top_panel", "visible", false);
		scene.instanceSet("three_five_inchinterior_back", "visible", false);
      	scene.instanceSet("hdd_12", "visible", true); 
		scene.instanceSet("PCI_bacck", "visible", true);
		scene.clearRefine();
        
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(6.180231072275836,1.5079644737231006,-24.696843982475066,0.866810920613501,32.0655782039611,800);
          
        }, 500)); 
        
          timeouts.push(setTimeout(function(){
               $("#point10text").fadeIn(400);
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 1100));  
    }

  scene.clearRefine();
    
}

function menu12Fadeout() {
    
   $("#point12image2,#point12image3,#point12image4,#point12image5").stop();
     $("#point12image2,#point12image3,#point12image4,#point12image5").css({"top":"155px","left":"421px"});
    
     $("#point12image2 img,#point12image3 img,#point12image4 img,#point12image5 img").stop();
     $("#point12image2 img,#point12image3 img,#point12image4 img,#point12image5 img").css({"width":"250px","height":"529px"});
    
        $("#point12image2 img").fadeOut(1);
        $("#point12text5").fadeOut(1);
        $("#point12text6").fadeOut(1);
        $("#point12image3 img").fadeOut(1);
        $("#point12text10").fadeOut(1);
        $("#point12text11").fadeOut(1);
        $("#point12image4 img").fadeOut(1);
        $("#point12text15").fadeOut(1);
        $("#point12image5 img").fadeOut(1);
        $("#point12text12").fadeOut(1);
    
        $("#point12text1").fadeIn(500);
        $("#point12image1 img").fadeIn(500);
        $("#point12image1_1 img").fadeIn(500);
        $("#point12image1_2 img").fadeIn(500);
        $("#point12image1_3 img").fadeIn(500);
        $("#point12image1_4 img").fadeIn(500);
    
}


var menu12Clicked=false;
var notrepeat = true;

function menu12Click() {
    console.log("menu12Clicked");
    $("#cpHeading").html("Lenovo Data Center Services");
    $("#dummy-canvas").css("pointer-events","none");
    $("#rightAnim").css('display','none');
	$("#point10text").css('display','none');
    $("#point12text").css('display','block');
	notrepeat = true;
    objectHide();
	mouseDownHide();
    menu12Fadeout();
    scene.instanceSet("SR655", "visible", false);
    scene.clearRefine();
       timeouts.push(setTimeout(function(){
         console.log("in_timeout_1");
        $("#point12text").css('display','block');
        $("#point12text2").fadeIn(10);
        $("#point12text3").fadeIn(10);
        $("#point12text4").fadeIn(10);
        $("#point12text7").fadeIn(10);
     }, 1000)); 
    
      //    slide2
    if(menu12Clicked){
         point12anim1();
    }else{
        timeouts.push(setTimeout(function(){
          point12anim1();
      },1000));
       
    }
    
    //    slide 3 start
//     timeouts.push(setTimeout(function(){
//          point12anim2();
//      },6000));

    // slide 4 start   
//      timeouts.push(setTimeout(function(){
//          point12anim3();
//      },11000));
    
       // slide 5 start   
//      timeouts.push(setTimeout(function(){
//          point12anim4();
//      },24000));
    
    timeouts.push(setTimeout(function(){
         animComplete();  
      },1000));

    timeouts.push(setTimeout(function(){
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 12000));
    
      scene.clearRefine();
      menu12Clicked=true;
}


function point12anim1(){
     timeouts.push(setTimeout(function(){
        $("#point12image2 img").fadeIn(500);
     }, 500)); 
    
    timeouts.push(setTimeout(function(){
        $("#point12image2 img").fadeIn(500);
        $("#point12image2 img").animate({width:"337px",height:"714px"},1000);
        $("#point12image2").animate({top:"106px",left:"389px"},1000);
        $("#point12text2").fadeOut(500);
        $("#point12image1_1 img").fadeOut(800);
     }, 1000));    
    
    timeouts.push(setTimeout(function(){
        $("#point12text5").fadeIn(500);
        $("#point12text6").fadeIn(500);
    }, 2000));
    
    timeouts.push(setTimeout(function(){
        $("#point12image2").animate({"top":"155px","left":"421px"},1000);
        $("#point12image2 img").animate({"width":"250px","height":"529px"},1000);
         $("#point12text5").fadeOut(500);
         $("#point12text6").fadeOut(500);
    }, 4000));  
    
     timeouts.push(setTimeout(function(){         
         $("#point12text2").fadeIn(500);
         $("#point12image1_1 img").fadeIn(500);
         $("#point12image2 img").fadeOut(500);
     }, 5000));
	 timeouts.push(setTimeout(function(){
		 if(notrepeat){	 
          point12anim2();
		 }
      },6000));

}

function point12anim2(){
 
    timeouts.push(setTimeout(function(){
        $("#point12image3 img").fadeIn(500);
    }, 500));
    
    timeouts.push(setTimeout(function(){
        $("#point12image3 img").fadeIn(500);
        $("#point12image3 img").animate({width:"337px",height:"714px"},1000);
        $("#point12image3").animate({top:"69px",left:"385px"},1000);
        $("#point12text3").fadeOut(500);
        $("#point12image1_2 img").fadeOut(800);
     }, 1000));
 
    timeouts.push(setTimeout(function(){
        $("#point12text10").fadeIn(500);
        $("#point12text11").fadeIn(500);
    }, 2000)); 
    
    timeouts.push(setTimeout(function(){
        $("#point12image3").animate({"top":"155px","left":"420px"},1000);
        $("#point12image3 img").animate({"width":"250px","height":"529px"},1000);
        $("#point12text10").fadeOut(500);
        $("#point12text11").fadeOut(500);
    }, 4000));
    
    timeouts.push(setTimeout(function(){
       $("#point12text3").fadeIn(500);
       $("#point12image1_2 img").fadeIn(500);
       $("#point12image3 img").fadeOut(500);
    }, 5000)); 
	timeouts.push(setTimeout(function(){
         if(notrepeat){	 
          point12anim3();
		 }
    },6000));
}

function point12anim3(){
    timeouts.push(setTimeout(function(){
        $("#point12image4 img").fadeIn(500);
    }, 500));

    timeouts.push(setTimeout(function(){
        $("#point12image4 img").animate({width:"330px",height:"699px"},1000);
        $("#point12image4").animate({top:"47px",left:"392px"},1000);
        $("#point12image4 img").fadeIn(1000);
        $("#point12text4").fadeOut(500);
        $("#point12image1_3 img").fadeOut(800);
    }, 1000));    

    timeouts.push(setTimeout(function(){
        $("#point12text15").fadeIn(500);
    }, 2000)); 
    
    timeouts.push(setTimeout(function(){
        $("#point12image4").animate({"top":"155px","left":"420px"},1000);
        $("#point12image4 img").animate({"width":"250px","height":"529px"},1000);
        $("#point12text15").fadeOut(500);
    }, 4000));
    
    timeouts.push(setTimeout(function(){
       $("#point12image4 img").fadeOut(500);
       $("#point12image1_3 img").fadeIn(100);
       $("#point12text4").fadeIn(100);
    }, 5000));
	timeouts.push(setTimeout(function(){
         if(notrepeat){	 
          point12anim1();
		 }
    },6000));
}

//function point12anim4(){
//    timeouts.push(setTimeout(function(){
//        $("#point12image5 img").fadeIn(500);
//    }, 500));
//    
//    timeouts.push(setTimeout(function(){
//        $("#point12image5 img").animate({width:"326px",height:"690px"},2000);
//        $("#point12image5").animate({top:"33px",left:"395px"},2000);
//        $("#point12image5 img").fadeIn(1000);
//        $("#point12text7").fadeOut(500);
//        $("#point12image1_4 img").fadeOut(800);
//    }, 1000));    
//
//    timeouts.push(setTimeout(function(){
//        $("#point12text12").fadeIn(500);
//    }, 2000)); 
//    
//    timeouts.push(setTimeout(function(){
//        $("#point12image5").animate({"top":"155px","left":"420px"},2500);
//        $("#point12image5 img").animate({"width":"250px","height":"529px"},2500);
//        $("#point12text12").fadeOut(500);
//    }, 5500));
//    
//    timeouts.push(setTimeout(function(){
//       $("#point12image5 img").fadeOut(500);
//       $("#point12image1_4 img").fadeIn(100);
//       $("#point12text7").fadeIn(100);
//    }, 7500));
//}

//menu13 - submenu of menu4
function menu13Click(){
  console.log("menu13Clicked");
    animStoped=false;
	$("#menu13").removeClass("disabled");
    $("#menu13").removeClass('active');
    $(".greyOutBox").removeClass('redOutBox');
    $("#menu13 .greyOutBox").addClass('redOutBox');
    $("#cpHeading").html("Maximum 3.5&quot; drive configuration: 20x 3.5&quot; 12(F)+4(M)+4(R)"); 
	$("#onloadCopy").css('display','none');
	      
if(!topCover){
        console.log("if...")
        
        objectHide();
      	scene.instanceSet("hdd_12", "visible", true);
		scene.instanceSet("three_five_inchinterior_back", "visible", true);
		scene.instanceSet("PCI_bacck", "visible", false);
		scene.instanceSet("NVME_back_01", "visible", false);
		scene.clearRefine();
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(0.43555749252547826,0.07944633891667634,-4.80601296937878,2.194984328536714,111.61723332986423,800);
          
        }, 300)); 
        
       timeouts.push(setTimeout(function(){
            scene.animPlayInTime("top_panel", 1, 1000);
            scene.clearRefine(); 
		    }, 1100)); 
        timeouts.push(setTimeout(function(){
			scene.instanceSet("top_panel", "visible", false);
            scene.animPlayInTime("HDD_CAGE", 1, 1000);
            scene.animPlayInTime("HDD_Handle", 1, 1000);
			scene.clearRefine();
			$("#point13text").css('display','block');
        }, 2100));  
        
        timeouts.push(setTimeout(function(){
            topCover = true;
//            $("#point4text").fadeIn(400);
             
        }, 3100));  
        
                
      timeouts.push(setTimeout(function(){
               
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 4100));  
        
    }else{
		objectHide();
        console.log("else...")
        topCover = true;
        scene.instanceSet("top_panel", "visible", false); 
//        scene.animPlayInTime("HDD_CAGE", 1, 10);
//        scene.animPlayInTime("HDD_Handle", 1, 10);
		scene.instanceSet("hdd_12", "visible", true);
		scene.instanceSet("PCI_bacck", "visible", false);
		scene.instanceSet("NVME_back_01", "visible", false);
		scene.instanceSet("three_five_inchinterior_back", "visible", true);
        scene.clearRefine();
        
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(0.43555749252547826,0.07944633891667634,-4.80601296937878,2.194984328536714,111.61723332986423,800);
          
        }, 300)); 
		
		 timeouts.push(setTimeout(function(){
            scene.animPlayInTime("HDD_CAGE", 1, 1000);
            scene.animPlayInTime("HDD_Handle", 1, 1000); 
			scene.clearRefine();
			$("#point13text").css('display','block');
        }, 1100)); 
        
          timeouts.push(setTimeout(function(){
//               $("#point4text").fadeIn(400);
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 2100));  
    }

  scene.clearRefine();  
}

//menu14 - submenu of menu8
function menu14Click() {
     animStoped = false;
     console.log("menu_14_clicked");
     $("#cpHeading").html("Storage-Rich Configuration");
     $("#onloadCopy").css("opacity","0").fadeOut(400); 
	 $("#menu14").removeClass("disabled");
     $("#menu14").removeClass('active');
     $(".greyOutBox").removeClass('redOutBox');
     $("#menu14 .greyOutBox").addClass('redOutBox');
    
    if(!topCover){
        console.log("if...")
        
		
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(0.43555749252547826,0.07944633891667634,-4.80601296937878,2.194984328536714,111.61723332986423,800);
          
        }, 300)); 
        timeouts.push(setTimeout(function(){
			scene.instanceSet("HDD_CAGE_SR655", "visible", true);
			objectHide();
			scene.instanceSet("HDD_2_5_", "visible", true);
			scene.clearRefine();
        }, 600));
        timeouts.push(setTimeout(function(){
            scene.animPlayInTime("top_panel", 1, 1000);
            scene.clearRefine(); 
        }, 1100)); 
		
		timeouts.push(setTimeout(function(){
			scene.instanceSet("top_panel", "visible", false);
			scene.animPlayInTime("group156", 1, 1000);
            scene.animPlayInTime("HDD_CAGE_SR655", 1, 1000);
//			$("#point8text").fadeIn(400);
			scene.clearRefine();
			$("#point14text").css('display','block');
        }, 2100));  
        
        timeouts.push(setTimeout(function(){
            topCover = true;
            
            scene.instanceSet("PCI_bacck", "visible", false);
            scene.instanceSet("hdd_12", "visible", false);
            scene.instanceSet("NVME_back_01", "visible", true);
            scene.instanceSet("HDD_2_5_", "visible", true);
            scene.clearRefine();  
        }, 1500));  
        
                
      timeouts.push(setTimeout(function(){
               
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 4100));  
        
    }else{
		objectHide();
        console.log("else...")
        topCover = true;
        scene.instanceSet("top_panel", "visible", false);
        scene.instanceSet("hdd_12", "visible", false);
        scene.instanceSet("HDD_2_5_", "visible", true);
		scene.instanceSet("three_five_inchinterior_back", "visible", false);
		scene.instanceSet("PCI_bacck", "visible", false);
		scene.instanceSet("NVME_back_01", "visible", true);
        scene.clearRefine();
        
        timeouts.push(setTimeout(function(){ 
        scene.gotoPosInTime(0.43555749252547826,0.07944633891667634,-4.80601296937878,2.194984328536714,111.61723332986423,800);
          
        }, 300)); 
         
		timeouts.push(setTimeout(function(){ 
			scene.animPlayInTime("group156", 1, 1000);
			scene.animPlayInTime("HDD_CAGE_SR655", 1, 1000);
			scene.clearRefine();
			$("#point14text").css('display','block');
		}, 1100)); 
		
          timeouts.push(setTimeout(function(){
//               $("#point8text").fadeIn(400);
            if(autoplayAnim){
             animCompeteAuto();
           }else{
               animComplete();         
           }
              
      }, 2100));  
    }

  scene.clearRefine();
}



var timeouts = [];

// Autp Play function

function autoPlayAllAnimations(){
    console.log("Stopped", animStoped, clickEventActive);    
  if (!animStoped || (!clickEventActive && !autoRotateState)) return;
    $("#rightAnim").animate({right: '-235px'}, "slow");
	scene.instanceSet("SR655", "visible", true);
        rightAnimToggle = true;
    $(".menuitems").removeClass('active');
    $("#rightAnim").css("display","block"); 
    $(".greyOutBox").removeClass('redOutBox');
    clearInterval(autoRotateInterval);
    clearTimeout(myVar);
    clearTimeout(autoPlayInt);
    clearTimeout(startAutorot); 
    $("#dummy-canvas").css("pointer-events","all");
    scene.instanceSet("SR850","visible",true);
    scene.clearRefine();
    for (var i=0; i<timeouts.length; i++) {
			              clearTimeout(timeouts[i]);
			                      }
                         timeouts =[];
    
    for (var i=0; i<timeoutsnew.length; i++) {
			              clearTimeout(timeoutsnew[i]);
			                      }
                         timeoutsnew =[];
    

	    firstAnim = true;
        autoplayAnim = true;
            for (var j = 1; j <= 11; j++) {  $('#point12text').css('display','none');translateOut(j);}
        $("#autoPlays").removeClass('playAll').off('click.playAll').addClass("pauseAll");
        $("#autoPlays .menuText").html("Stop");
        $("#pauseplayImg").css("display","none");
        $("#pauseplayImg2").css("display","block");
        $("#pauseplayImg2 img").attr("src" ,"./images_gl/Pause.svg").css("height","13px");

//        objectHide();
//        reversAll();
//        tooltipCheckbtn();
//        if(currneAnim == 10){
//            currneAnim = 11;
//        }
//        if(currneAnim == 12){
//            currneAnim = 10;
//        }
     
    
        if(currneAnim< 15){
			if(currneAnim == 4){
            	currneAnim = 13;
            	AutoPlayMenus(currneAnim);
			 }else if(currneAnim == 13){
            	currneAnim = 5;
            	AutoPlayMenus(currneAnim); 
			 }else if(currneAnim == 8){
            	currneAnim = 14;
            	AutoPlayMenus(currneAnim);
        	}else if(currneAnim == 14){
				currneAnim = 9;
				AutoPlayMenus(currneAnim);
        	}else if(currneAnim == 11){
                if(autoplayCatalog){
                    scene.stop();
                    $(window.parent).unbind('resize');
                    window.top.document.getElementById("mainpanel2").contentWindow.openSuperblazeAuto();
                    $("#superblazeIframe",window.parent.document).css('display','none');
                    window.top.document.getElementById("mainpanel2").contentWindow.superblazeClosed();
                    currentAnimation = 1;
                } else{
				currneAnim = 2;
				AutoPlayMenus(currneAnim);
            }
			}else{
            console.log("currneAnim"+currneAnim);  
            currneAnim++;
            AutoPlayMenus(currneAnim);
			}
        }else{
            // currneAnim = 2;
            // AutoPlayMenus(currneAnim); 
            if(autoplayCatalog){
                    scene.stop();
                    $(window.parent).unbind('resize');
                    window.top.document.getElementById("mainpanel2").contentWindow.openSuperblazeAuto();
                    $("#superblazeIframe",window.parent.document).css('display','none');
                    window.top.document.getElementById("mainpanel2").contentWindow.superblazeClosed();
                    currentAnimation = 1;
                } else{
                currneAnim = 2;
                AutoPlayMenus(currneAnim);
            }
        }
    
    console.log("play", currneAnim);
}


function autoPauseAllAnimations(){
    console.log("pause");
    clearTimeout(autoPlayInt);  
    $("#autoPlays").removeClass('pauseAll').off('click.pauseAll').addClass("playAll");
    $("#autoPlays .menuText").html("Play All");
    $("#pauseplayImg2").css("display","none");
    $("#pauseplayImg").css("display","block");
    $("#pauseplayImg img").attr("src" ,"./images_gl/Play.svg").css("height","14px");
//    $(".menuitems").css("background-color","").css("opacity","");
    autoplayAnim = false;
     if(autoplayAnim){
               setTimeout(function(){                       
                    autoplayAnim = false;
                     var newId = "#menu"+currneAnim;
                     $("#menu"+currneAnim).addClass("active").css("background-color","#eb140a").css("opacity","1");

                },50);

        }
//    for (var i=0; i<timeouts.length; i++) {
//			clearTimeout(timeouts[i]);
//     }
//    timeouts = [];

        clearTimeout(autoPlayInt);

  setTimeout(function(){
      animComplete();
  },2000);
}

var autoPlayInt
function animCompeteAuto(){
    console.log("calleAuto");
        animStoped = true;
    g_navEnabled = true;
 autoPlayInt =    setTimeout(function(){ 
      console.log("stopped");
          autoPlayAllAnimations();
        }, 9500);
}

function AutoPlayMenus(currneAnim){    
    $(".menuitems").css("background-color","").css("opacity","");
    clearInterval(autoRotateInterval);
    clearInterval(myVar); 
    clearTimeout(startAutorot); 
	reversAll();  
     prevAnimation=currneAnim;
    $("h3#menu"+currneAnim).css("background-color","#eb140a").css("opacity","1");
     for (var j = 1; j <= 11; j++) {translateOut(j);}
//     $( "#accordion" ).accordion( "option", "disabled", true );
    console.log("currneAnim");
     switch ("menu"+currneAnim) {
                                        case "menu2":
                                        $("#accordion" ).accordion( "option", "active", false );
                                        menu2Click();
                                        break;
                                        case "menu3":
//                                        $( "#accordion" ).accordion( "option", "active", 2);
                                        menu3Click();
                                        break;
                                        case "menu4": 
                                        menu4Click();
                                        $( "#accordion" ).accordion( "option", "active",3 );     
                                        break;
                                        case "menu5":
                                        menu5Click();
                                        break;
                                        case "menu6":
                                        menu6Click();
                                        $( "#accordion" ).accordion( "option", "active",4);     
                                        break;
                                        case "menu7":
                                        menu7Click();
                                        break;
                                        case "menu8":
                                        menu8Click();
                                        $( "#accordion" ).accordion( "option", "active",5);     
                                        break;
                                        case "menu9":
                                        menu9Click();
                                        break;
                                        case "menu10":
                                        $( "#accordion" ).accordion( "option", "active", false );
                                        menu10Click();
                                        break;
                                        case "menu11":
                                        $( "#accordion" ).accordion( "option", "active", false );
                                        menu12Click();
                                        break;
		 								case "menu13":
                                        menu13Click();
                                        break;
			 							case "menu14":
                                        menu14Click();
                                        break;
                                       
            }
}

function animComplete() {
    setTimeout(function(){
//        $( "#accordion" ).accordion( "option", "disabled", false );
    animStoped = true;
    scene._navEnabled = true;
    },1500)
}

function reversAll(){
	clearInt();
	$("#Menu2text").css("display","none");
	$("#adhoc_meet_img").css("display","none");
	$("#schedule_meet_div").css("display","none");
    
    scene.instanceSet("SR850","visible",true);
    scene.clearRefine();
    
    $("#point12text1").fadeOut(10);
    $("#point12text2").fadeOut(10);
    $("#point12text3").fadeOut(10);
    $("#point12text4").fadeOut(10);
    $("#point12image1 img").fadeOut(10);
    $("#point12text5").fadeOut(10);
    $("#point12text6").fadeOut(10);
    $("#point12text7").fadeOut(10);
    $("#point12text8").fadeOut(10);
    $("#point12image2 img").fadeOut(10);
    $("#point12text9").fadeOut(10);
    $("#point12text10").fadeOut(10);
    $("#point12text11").fadeOut(10);
    $("#point12text12").fadeOut(10);
    $("#point12image3 img").fadeOut(10);
    $("#point12text13").fadeOut(10);
    $("#point12text14").fadeOut(10);
    $("#point12text15").fadeOut(10);
    $("#point12image4 img").fadeOut(10);
}

var imgInterval;


function clearInt() {
   clearInterval(imgInterval);
	// $("#imageContainerimg").attr('src','');
	$("#imageContainerimg").attr('src','images_gl/ring_animation/1.png');
	$("#imageContainerimg").css("display","none");
}

function close_window(){
   close();
}

document.onselectstart = function() {
    return false;
};

var btnDrag = false;

function mouseOverBtnDrag() {
    btnDrag = true;
}

function mouseOutBtnDrag() {
    setTimeout(function() {
        btnDrag = false;
    }, 100);
}

var updateId = 0;

function onRightClick(event) {
    ////console.log("press right");
    //mdown = true;
    //panNav = true;
    return false; //surpress theright menu 
}
function onWindowFocus() {
    updateEnabled = true;
}

function onWindowBlur() {
    updateEnabled = false;
}

function debounce(func, wait, immediate, ev) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

function frameUpdate () {
   window.requestAnimationFrame(frameUpdate);
   if (scene._refineCount < 64) frameUpdateForScene(scene);
     if(clickEventActive || autoRotateState){
        $(".menuitems, #autoPlays").css("pointer-events","all");

    }else if(!clickEventActive){
//        console.log(">>>", clickEventActive);
        $(".menuitems, #autoPlays").css("pointer-events","none");
    }
//       if(clickEventActive){
//           $( "#accordion" ).accordion( "option", "disabled", false );
//       }else{
//                            $( "#accordion" ).accordion( "option", "disabled", true );
//       }
// console.log(scene._nav._navYAng+","+scene._nav._navXAng+","+scene._nav._navPan[0]+","+scene._nav._navPan[1]+","+scene._nav._navDolly);
//   
//     if (yPos < yEnd && mdown != true && yStarted) {
//					autoRotateState = true;
//					if (yPos > yEnd - 2) yPos = 0;
//						if(new_R){
//							autoRotateStop();
//						}else{
//							autoRotateRequest();
//						}
//     }else yStarted = false;
	
//		 if(rotating[0] != 0 || rotating[1] != 0){
//				if (rSpeed < 0){
//					rSpeed = 0;
//					rAcc = rAccelaration;
//					rotating = [0,0];
//				}
//				rSpeed = (rSpeed < rMaxSpeed || rAcc< 0) ? rSpeed+rAcc : rSpeed;
//				console.log(rSpeed);
//				scene._nav.NavRotation([0,0], [rotating[0]*rSpeed, rotating[1]*rSpeed]);
				//scene.clearRefine();
}

function frameUpdateForScene(scene) {
    var bgotoPosInTimeUpdate = scene._nav._navgotoPosInTimeActive;
    sceneViewMatrix = scene._nav.NavCreateViewMatrix(scene._initialNavMatrix);
    scene.setViewMatrix(sceneViewMatrix);
    scene.setModelMatrix(scene._nav.NavCreateModelMatrix(scene._initialNavMatrix));
    drawn = scene.draw();
    if (bgotoPosInTimeUpdate)
    scene.clearRefine();
	if (drawn) hotspotPosAsignment();
}

function getScene(ev) {
		    var s = scene;
		    if (scene2 != null && ev.currentTarget == canvas2)
		        s = scene2;
		    return s;
}




/*------------auto rotate functionality------------*/
var yPos = 0;
var yEnd = 300;
var yStarted = false;
var autoRotateState = false;
var yLevel = 0;
var yStep = [1];
var ySpeed = [20];
var myVar;
var autoRotateInterval;

function autoRotate(){
//    console.log("autorotate")
       if ((navigator.userAgent.indexOf("iPhone") != -1) || ((navigator.userAgent.indexOf("Android") != -1) || (navigator.userAgent.indexOf("Mobile") != -1)) || (navigator.userAgent.indexOf('iPad') != -1) || (navigator.userAgent.indexOf('iPod') != -1)) {
        
    animStoped = true;
           
      scene._navEnabled = true;
        } else if (autoplayAnim == true) {
            animStoped = true;
      scene._navEnabled = true;
            autoRotateState = false;
        }
        else
        {
            yPos = 0;
//            console.log('rotate', yStarted);
            if (!yStarted)
                
//             autoRotateRequest();
            if(autoRotateState){
              autoRotateInterval =setInterval(function(){
//                  console.log('rotate');
                    autoRotateRequest();
               },10);    
            }
               
               
               
        }
                
}


var autoRotateInterval;
function autoRotateStop() {
    yPos = yEnd;
    autoRotateState = false;
    yStarted = false;
    clearInterval(autoRotateInterval);
    clearTimeout(autoPlayInt);                      
    clearTimeout(myVar);                      
    clearTimeout(startAutorot);
    
}   

 function autoRotateRequest(ev) {
     var s = getScene(ev);

     yStarted = true;
                yPos += 1;
                var mpos = [ 0.0, 0.0 ];
                var mdelta = [0.50,0.0];
              if (s._nav.NavRotation(mpos, mdelta)){   
//                  console.log("calle")
                    scene.clearRefine();
              }
 }

function autoRotateCall() {
        myVar = setTimeout(function(){
            autoRotateState = true; 
                autoRotate();
        }, 10);
}

/*end*/




var hotspotPoint = true;
var hotspotOn;
var clockWise=true;
var antiClockWise=false;

function hotspotPosAsignment() {
    
    var viewCameraZV = [sceneViewMatrix[8], sceneViewMatrix[9], sceneViewMatrix[10]];
     var hotspotopacityspeed = 3.0;
	
	if(sceneViewMatrix[14] >1.6 && sceneViewMatrix[14] < 9 && sceneViewMatrix[12] >16 && sceneViewMatrix[12] < 120){
		$('#hotspot1,#hotspot2,#hotspot3,#hotspot4,#hotspot12,#hotspot13,#hotspot14,#hotspot15,#hotspot16,#hotspot114').css('display','block');
	}else{
		$('#hotspot1,#hotspot2,#hotspot3,#hotspot4,#hotspot12,#hotspot13,#hotspot14,#hotspot15,#hotspot16,#hotspot114').css('display','none');
	}
	if(sceneViewMatrix[14] >1 && sceneViewMatrix[14] < 8 && sceneViewMatrix[12] >10 && sceneViewMatrix[12] < 83){
		$('#hotspot5,#hotspot6,#hotspot7,#hotspot8,#hotspot9,#hotspot10,#hotspot11,#hotspot111').css('display','block');
	}else{
		$('#hotspot5,#hotspot6,#hotspot7,#hotspot8,#hotspot9,#hotspot10,#hotspot11,#hotspot111').css('display','none');
	}
	
//	if(sceneViewMatrix[14] >-181 && sceneViewMatrix[14] < -179 && sceneViewMatrix[12] >-5 && sceneViewMatrix[12] < 25){
//		$('#hotspot17,#hotspot18,#hotspot19,#hotspot20,#hotspot21,#hotspot22,#hotspot23,#hotspot24,#hotspot25,#hotspot26,#hotspot27,#hotspot28,#hotspot29,#hotspot30,#hotspot31,#hotspot32,#hotspot33,#hotspot34,#hotspot35,#hotspot36,#hotspot37,#hotspot38,#hotspot39,#hotspot40,#hotspot41,#hotspot42,#hotspot43').css('display','block');
//	}else{
//		$('#hotspot17,#hotspot18,#hotspot19,#hotspot20,#hotspot21,#hotspot22,#hotspot23,#hotspot24,#hotspot25,#hotspot26,#hotspot27,#hotspot28,#hotspot29,#hotspot30,#hotspot31,#hotspot32,#hotspot33,#hotspot34,#hotspot35,#hotspot36,#hotspot37,#hotspot38,#hotspot39,#hotspot40,#hotspot41,#hotspot42,#hotspot43').css('display','none');
//	}
	

        var pos2Dpoint1 = [];                      
        var norm3Dpoint1 = scene.getObjectNormal("Hotspot_1Shape-0");
        var hotspotopacity1 = infinityrt_dp(norm3Dpoint1, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity1>0 && (hotspotOn == true )) hotspotopacity1=0;
        if (hotspotopacity1 < 0.0) hotspotopacity1 = 0.0;
        else if (hotspotopacity1 > 1.0) hotspotopacity1 = 1.0;
//        if(hotspotopacity1==0)$("#hotspot1", window.document).css('visibility','hidden');
//        else $("#hotspot1", window.document).css('visibility','visible');
        pos2Dpoint1 = scene.projectPoint(scene.getObjectLocation("Hotspot_1Shape-0", true));

        var pos2Dpoint2 = [];
        var norm3Dpoint2 = scene.getObjectNormal("Hotspot_2Shape-0");
        var hotspotopacity2 = infinityrt_dp(norm3Dpoint2, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity2>0 && (hotspotOn == true )) hotspotopacity2=0;
        if (hotspotopacity2 < 0.0) hotspotopacity2 = 0.0;
        else if (hotspotopacity2 > 1.0) hotspotopacity2 = 1.0;
//        if(hotspotopacity2==0)$("#hotspot2", window.document).css('visibility','hidden');
//        else $("#hotspot2", window.document).css('visibility','visible');
        pos2Dpoint2 = scene.projectPoint(scene.getObjectLocation("Hotspot_2Shape-0", true));



        var pos2Dpoint3 = [];
        var norm3Dpoint3 = scene.getObjectNormal("Hotspot_3Shape-0");
        var hotspotopacity3 = infinityrt_dp(norm3Dpoint3, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity3>0 && (hotspotOn == true )) hotspotopacity3=0;
        if (hotspotopacity3 < 0.0) hotspotopacity3 = 0.0;
        else if (hotspotopacity3 > 1.0) hotspotopacity3 = 1.0;
//        if(hotspotopacity3==0)$("#hotspot3", window.document).css('visibility','hidden');
//        else $("#hotspot3", window.document).css('visibility','visible');
        pos2Dpoint3 = scene.projectPoint(scene.getObjectLocation("Hotspot_3Shape-0", true));


        var pos2Dpoint4 = [];
        var norm3Dpoint4 = scene.getObjectNormal("Hotspot_4Shape-0");
        var hotspotopacity4 = infinityrt_dp(norm3Dpoint4, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity4>0 && (hotspotOn == true )) hotspotopacity4=0;
        if (hotspotopacity4 < 0.0) hotspotopacity4 = 0.0;
        else if (hotspotopacity4 > 1.0) hotspotopacity4 = 1.0;
//        if(hotspotopacity4==0)$("#hotspot4", window.document).css('visibility','hidden');
//        else $("#hotspot4", window.document).css('visibility','visible');
        pos2Dpoint4 = scene.projectPoint(scene.getObjectLocation("Hotspot_4Shape-0", true));


        var pos2Dpoint5 = [];
        var norm3Dpoint5 = scene.getObjectNormal("Hotspot_5Shape-0");
        var hotspotopacity5 = infinityrt_dp(norm3Dpoint5, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity5>0 && (hotspotOn == true )) hotspotopacity5=0;
        if (hotspotopacity5 < 0.0) hotspotopacity5 = 0.0;
        else if (hotspotopacity5 > 1.0) hotspotopacity5 = 1.0;
//        if(hotspotopacity5==0)$("#hotspot5", window.document).css('visibility','hidden');
//        else $("#hotspot5", window.document).css('visibility','visible');
        pos2Dpoint5 = scene.projectPoint(scene.getObjectLocation("Hotspot_5Shape-0", true));

        var pos2Dpoint6 = [];
        var norm3Dpoint6 = scene.getObjectNormal("Hotspot_6Shape-0");
        var hotspotopacity6 = infinityrt_dp(norm3Dpoint6, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity6>0 && (hotspotOn == true )) hotspotopacity6=0;
        if (hotspotopacity6 < 0.0) hotspotopacity6 = 0.0;
        else if (hotspotopacity6 > 1.0) hotspotopacity6 = 1.0;
//        if(hotspotopacity6==0)$("#hotspot6", window.document).css('visibility','hidden');
//        else $("#hotspot6", window.document).css('visibility','visible');
        pos2Dpoint6 = scene.projectPoint(scene.getObjectLocation("Hotspot_6Shape-0", true));

        var pos2Dpoint7 = [];
        var norm3Dpoint7 = scene.getObjectNormal("Hotspot_7Shape-0");
        var hotspotopacity7 = infinityrt_dp(norm3Dpoint7, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity7>0 && (hotspotOn == true )) hotspotopacity7=0;
        if (hotspotopacity7 < 0.0) hotspotopacity7 = 0.0;
        else if (hotspotopacity7 > 1.0) hotspotopacity7 = 1.0;
//        if(hotspotopacity7==0)$("#hotspot7", window.document).css('visibility','hidden');
//        else $("#hotspot7", window.document).css('visibility','visible');
        pos2Dpoint7 = scene.projectPoint(scene.getObjectLocation("Hotspot_7Shape-0", true));

        var pos2Dpoint8 = [];
        var norm3Dpoint8 = scene.getObjectNormal("Hotspot_8Shape-0");
        var hotspotopacity8 = infinityrt_dp(norm3Dpoint8, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity8>0 && (hotspotOn == true )) hotspotopacity8=0;
        if (hotspotopacity8 < 0.0) hotspotopacity8 = 0.0;
        else if (hotspotopacity8 > 1.0) hotspotopacity8 = 1.0;
        if(hotspotopacity8==0)$("#hotspot8", window.document).css('visibility','hidden');
        else $("#hotspot8", window.document).css('visibility','visible');
        pos2Dpoint8 = scene.projectPoint(scene.getObjectLocation("Hotspot_8Shape-0", true));


        var pos2Dpoint9 = [];
        var norm3Dpoint9 = scene.getObjectNormal("Hotspot_9Shape-0");
        var hotspotopacity9 = infinityrt_dp(norm3Dpoint9, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity9>0 && (hotspotOn == true )) hotspotopacity9=0;
        if (hotspotopacity9 < 0.0) hotspotopacity9 = 0.0;
        else if (hotspotopacity9 > 1.0) hotspotopacity9 = 1.0;
//        if(hotspotopacity9==0)$("#hotspot9", window.document).css('visibility','hidden');
//        else $("#hotspot9", window.document).css('visibility','visible');
        pos2Dpoint9 = scene.projectPoint(scene.getObjectLocation("Hotspot_9Shape-0", true));

        var pos2Dpoint10 = [];
        var norm3Dpoint10 = scene.getObjectNormal("Hotspot_10Shape-0");
        var hotspotopacity10 = infinityrt_dp(norm3Dpoint10, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity10>0 && (hotspotOn == true )) hotspotopacity10=0;
        if (hotspotopacity10 < 0.0) hotspotopacity10 = 0.0;
        else if (hotspotopacity10 > 1.0) hotspotopacity10 = 1.0;
//        if(hotspotopacity10==0)$("#hotspot10", window.document).css('visibility','hidden');
//        else $("#hotspot10", window.document).css('visibility','visible');
        pos2Dpoint10 = scene.projectPoint(scene.getObjectLocation("Hotspot_10Shape-0", true));


        var pos2Dpoint11 = [];
        var norm3Dpoint11 = scene.getObjectNormal("Hotspot_11Shape-0");
        var hotspotopacity11 = infinityrt_dp(norm3Dpoint11, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity11>0 && (hotspotOn == true )) hotspotopacity11=0;
        if (hotspotopacity11 < 0.0) hotspotopacity11 = 0.0;
        else if (hotspotopacity11 > 1.0) hotspotopacity11 = 1.0;
//        if(hotspotopacity11==0)$("#hotspot11", window.document).css('visibility','hidden');
//        else $("#hotspot11", window.document).css('visibility','visible');
        pos2Dpoint11 = scene.projectPoint(scene.getObjectLocation("Hotspot_11Shape-0", true));
	
	var pos2Dpoint111 = [];
        var norm3Dpoint111 = scene.getObjectNormal("new_Hotspott_8Shape-0");
        var hotspotopacity111 = infinityrt_dp(norm3Dpoint111, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity111>0 && (hotspotOn == true )) hotspotopacity111=0;
        if (hotspotopacity111 < 0.0) hotspotopacity111 = 0.0;
        else if (hotspotopacity111 > 1.0) hotspotopacity111 = 1.0;
//        if(hotspotopacity111==0)$("#hotspot111", window.document).css('visibility','hidden');
//        else $("#hotspot111", window.document).css('visibility','visible');
        pos2Dpoint111 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_8Shape-0", true));

        var pos2Dpoint12 = [];
        var norm3Dpoint12 = scene.getObjectNormal("Hotspot_12Shape-0");
        var hotspotopacity12 = infinityrt_dp(norm3Dpoint12, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity12>0 && (hotspotOn == true )) hotspotopacity12=0;
        if (hotspotopacity12 < 0.0) hotspotopacity12 = 0.0;
        else if (hotspotopacity12 > 1.0) hotspotopacity12 = 1.0;
//        if(hotspotopacity12==0)$("#hotspot12", window.document).css('visibility','hidden');
//        else $("#hotspot12", window.document).css('visibility','visible');
        pos2Dpoint12 = scene.projectPoint(scene.getObjectLocation("Hotspot_12Shape-0", true));


        var pos2Dpoint13 = [];
        var norm3Dpoint13 = scene.getObjectNormal("Hotspot_13Shape-0");
        var hotspotopacity13 = infinityrt_dp(norm3Dpoint13, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity13>0 && (hotspotOn == true )) hotspotopacity13=0;
        if (hotspotopacity13 < 0.0) hotspotopacity13 = 0.0;
        else if (hotspotopacity13 > 1.0) hotspotopacity13 = 1.0;
//        if(hotspotopacity13==0)$("#hotspot13", window.document).css('visibility','hidden');
//        else $("#hotspot13", window.document).css('visibility','visible');
        pos2Dpoint13 = scene.projectPoint(scene.getObjectLocation("Hotspot_13Shape-0", true));


        var pos2Dpoint14 = [];
        var norm3Dpoint14 = scene.getObjectNormal("Hotspot_14Shape-0");
        var hotspotopacity14 = infinityrt_dp(norm3Dpoint14, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity14>0 && (hotspotOn == true )) hotspotopacity14=0;
        if (hotspotopacity14 < 0.0) hotspotopacity14 = 0.0;
        else if (hotspotopacity14 > 1.0) hotspotopacity14 = 1.0;
//        if(hotspotopacity14==0)$("#hotspot14", window.document).css('visibility','hidden');
//        else $("#hotspot14", window.document).css('visibility','visible');
        pos2Dpoint14 = scene.projectPoint(scene.getObjectLocation("Hotspot_14Shape-0", true));


        var pos2Dpoint15 = [];
        var norm3Dpoint15 = scene.getObjectNormal("Hotspot_15Shape-0");
        var hotspotopacity15 = infinityrt_dp(norm3Dpoint15, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity15>0 && (hotspotOn == true )) hotspotopacity15=0;
        if (hotspotopacity15 < 0.0) hotspotopacity15 = 0.0;
        else if (hotspotopacity15 > 1.0) hotspotopacity15 = 1.0;
//        if(hotspotopacity15==0)$("#hotspot15", window.document).css('visibility','hidden');
//        else $("#hotspot15", window.document).css('visibility','visible');
        pos2Dpoint15 = scene.projectPoint(scene.getObjectLocation("Hotspot_15Shape-0", true));


        var pos2Dpoint16 = [];
        var norm3Dpoint16 = scene.getObjectNormal("Hotspot_16Shape-0");
        var hotspotopacity16 = infinityrt_dp(norm3Dpoint16, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity16>0 && (hotspotOn == true )) hotspotopacity16=0;
        if (hotspotopacity16 < 0.0) hotspotopacity16 = 0.0;
        else if (hotspotopacity16 > 1.0) hotspotopacity16 = 1.0;
//        if(hotspotopacity16==0)$("#hotspot16", window.document).css('visibility','hidden');
//        else $("#hotspot16", window.document).css('visibility','visible');
        pos2Dpoint16 = scene.projectPoint(scene.getObjectLocation("Hotspot_16Shape-0", true));
	
	var pos2Dpoint114 = [];
        var norm3Dpoint114 = scene.getObjectNormal("new_Hotspott_8Shape-0");
        var hotspotopacity114 = infinityrt_dp(norm3Dpoint114, viewCameraZV) * hotspotopacityspeed-2.9;
        if(hotspotopacity114>0 && (hotspotOn == true )) hotspotopacity114=0;
        if (hotspotopacity114 < 0.0) hotspotopacity114 = 0.0;
        else if (hotspotopacity114 > 1.0) hotspotopacity114 = 1.0;
//        if(hotspotopacity114==0)$("#hotspot114", window.document).css('visibility','hidden');
//        else $("#hotspot114", window.document).css('visibility','visible');
        pos2Dpoint114 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_8Shape-0", true));
	
	
		//17-43
	var pos2Dpoint17 = [];
        var norm3Dpoint17 = scene.getObjectNormal("Hotspott_1Shape-0");
        var hotspotopacity17 = infinityrt_dp(norm3Dpoint17, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity17>0 && (hotspotOn == true )) hotspotopacity17=0;
        if (hotspotopacity17 < 0.0) hotspotopacity17 = 0.0;
        else if (hotspotopacity17 > 1.0) hotspotopacity17 = 1.0;
        if(hotspotopacity17==0)$("#hotspot17", window.document).css('visibility','hidden');
        else $("#hotspot17", window.document).css('visibility','visible');
        pos2Dpoint17 = scene.projectPoint(scene.getObjectLocation("Hotspott_1Shape-0", true));
	
	var pos2Dpoint18 = [];
        var norm3Dpoint18 = scene.getObjectNormal("Hotspott_2Shape-0");
        var hotspotopacity18 = infinityrt_dp(norm3Dpoint18, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity18>0 && (hotspotOn == true )) hotspotopacity18=0;
        if (hotspotopacity18 < 0.0) hotspotopacity18 = 0.0;
        else if (hotspotopacity18 > 1.0) hotspotopacity18 = 1.0;
        if(hotspotopacity18==0)$("#hotspot18", window.document).css('visibility','hidden');
        else $("#hotspot18", window.document).css('visibility','visible');
        pos2Dpoint18 = scene.projectPoint(scene.getObjectLocation("Hotspott_2Shape-0", true));
	
	var pos2Dpoint19 = [];
        var norm3Dpoint19 = scene.getObjectNormal("Hotspott_3Shape-0");
        var hotspotopacity19 = infinityrt_dp(norm3Dpoint19, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity19>0 && (hotspotOn == true )) hotspotopacity19=0;
        if (hotspotopacity19 < 0.0) hotspotopacity19 = 0.0;
        else if (hotspotopacity19 > 1.0) hotspotopacity19 = 1.0;
        if(hotspotopacity19==0)$("#hotspot19", window.document).css('visibility','hidden');
        else $("#hotspot19", window.document).css('visibility','visible');
        pos2Dpoint19 = scene.projectPoint(scene.getObjectLocation("Hotspott_3Shape-0", true));
	
	var pos2Dpoint20 = [];
        var norm3Dpoint20 = scene.getObjectNormal("Hotspott_4Shape-0");
        var hotspotopacity20 = infinityrt_dp(norm3Dpoint20, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity20>0 && (hotspotOn == true )) hotspotopacity20=0;
        if (hotspotopacity20 < 0.0) hotspotopacity20 = 0.0;
        else if (hotspotopacity20 > 1.0) hotspotopacity20 = 1.0;
        if(hotspotopacity20==0)$("#hotspot20", window.document).css('visibility','hidden');
        else $("#hotspot20", window.document).css('visibility','visible');
        pos2Dpoint20 = scene.projectPoint(scene.getObjectLocation("Hotspott_4Shape-0", true));
	
	var pos2Dpoint21 = [];
        var norm3Dpoint21 = scene.getObjectNormal("Hotspott_5Shape-0");
        var hotspotopacity21 = infinityrt_dp(norm3Dpoint21, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity21>0 && (hotspotOn == true )) hotspotopacity21=0;
        if (hotspotopacity21 < 0.0) hotspotopacity21 = 0.0;
        else if (hotspotopacity21 > 1.0) hotspotopacity21 = 1.0;
        if(hotspotopacity21==0)$("#hotspot21", window.document).css('visibility','hidden');
        else $("#hotspot21", window.document).css('visibility','visible');
        pos2Dpoint21 = scene.projectPoint(scene.getObjectLocation("Hotspott_5Shape-0", true));
	
	var pos2Dpoint22 = [];
        var norm3Dpoint22 = scene.getObjectNormal("Hotspott_6Shape-0");
        var hotspotopacity22 = infinityrt_dp(norm3Dpoint22, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity22>0 && (hotspotOn == true )) hotspotopacity22=0;
        if (hotspotopacity22 < 0.0) hotspotopacity22 = 0.0;
        else if (hotspotopacity22 > 1.0) hotspotopacity22 = 1.0;
        if(hotspotopacity22==0)$("#hotspot22", window.document).css('visibility','hidden');
        else $("#hotspot22", window.document).css('visibility','visible');
        pos2Dpoint22 = scene.projectPoint(scene.getObjectLocation("Hotspott_6Shape-0", true));
	
	//new added 7
	var pos2Dpoint211 = [];
        var norm3Dpoint211 = scene.getObjectNormal("new_Hotspott_1Shape-0");
        var hotspotopacity211 = infinityrt_dp(norm3Dpoint211, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity211>0 && (hotspotOn == true )) hotspotopacity211=0;
        if (hotspotopacity211 < 0.0) hotspotopacity211 = 0.0;
        else if (hotspotopacity211 > 1.0) hotspotopacity211 = 1.0;
        if(hotspotopacity211==0)$("#hotspot211", window.document).css('visibility','hidden');
        else $("#hotspot211", window.document).css('visibility','visible');
        pos2Dpoint211 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_1Shape-0", true));
	
	var pos2Dpoint212 = [];
        var norm3Dpoint212 = scene.getObjectNormal("new_Hotspott_2Shape-0");
        var hotspotopacity212 = infinityrt_dp(norm3Dpoint212, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity212>0 && (hotspotOn == true )) hotspotopacity212=0;
        if (hotspotopacity212 < 0.0) hotspotopacity212 = 0.0;
        else if (hotspotopacity212 > 1.0) hotspotopacity212 = 1.0;
        if(hotspotopacity212==0)$("#hotspot212", window.document).css('visibility','hidden');
        else $("#hotspot212", window.document).css('visibility','visible');
        pos2Dpoint212 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_2Shape-0", true));
	
	var pos2Dpoint213 = [];
        var norm3Dpoint213 = scene.getObjectNormal("new_Hotspott_3Shape-0");
        var hotspotopacity213 = infinityrt_dp(norm3Dpoint213, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity213>0 && (hotspotOn == true )) hotspotopacity213=0;
        if (hotspotopacity213 < 0.0) hotspotopacity213 = 0.0;
        else if (hotspotopacity213 > 1.0) hotspotopacity213 = 1.0;
        if(hotspotopacity213==0)$("#hotspot213", window.document).css('visibility','hidden');
        else $("#hotspot213", window.document).css('visibility','visible');
        pos2Dpoint213 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_3Shape-0", true));
	
	var pos2Dpoint214 = [];
        var norm3Dpoint214 = scene.getObjectNormal("new_Hotspott_4Shape-0");
        var hotspotopacity214 = infinityrt_dp(norm3Dpoint214, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity214>0 && (hotspotOn == true )) hotspotopacity214=0;
        if (hotspotopacity214 < 0.0) hotspotopacity214 = 0.0;
        else if (hotspotopacity214 > 1.0) hotspotopacity214 = 1.0;
        if(hotspotopacity214==0)$("#hotspot214", window.document).css('visibility','hidden');
        else $("#hotspot214", window.document).css('visibility','visible');
        pos2Dpoint214 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_4Shape-0", true));
	
	var pos2Dpoint215 = [];
        var norm3Dpoint215 = scene.getObjectNormal("new_Hotspott_5Shape-0");
        var hotspotopacity215 = infinityrt_dp(norm3Dpoint215, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity215>0 && (hotspotOn == true )) hotspotopacity215=0;
        if (hotspotopacity215 < 0.0) hotspotopacity215 = 0.0;
        else if (hotspotopacity215 > 1.0) hotspotopacity215 = 1.0;
        if(hotspotopacity215==0)$("#hotspot215", window.document).css('visibility','hidden');
        else $("#hotspot215", window.document).css('visibility','visible');
        pos2Dpoint215 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_5Shape-0", true));
	
	var pos2Dpoint216 = [];
        var norm3Dpoint216 = scene.getObjectNormal("new_Hotspott_6Shape-0");
        var hotspotopacity216 = infinityrt_dp(norm3Dpoint216, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity216>0 && (hotspotOn == true )) hotspotopacity216=0;
        if (hotspotopacity216 < 0.0) hotspotopacity216 = 0.0;
        else if (hotspotopacity216 > 1.0) hotspotopacity216 = 1.0;
        if(hotspotopacity216==0)$("#hotspot216", window.document).css('visibility','hidden');
        else $("#hotspot216", window.document).css('visibility','visible');
        pos2Dpoint216 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_6Shape-0", true));
	
	var pos2Dpoint217 = [];
        var norm3Dpoint217 = scene.getObjectNormal("new_Hotspott_7Shape-0");
        var hotspotopacity217 = infinityrt_dp(norm3Dpoint217, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity217>0 && (hotspotOn == true )) hotspotopacity217=0;
        if (hotspotopacity217 < 0.0) hotspotopacity217 = 0.0;
        else if (hotspotopacity217 > 1.0) hotspotopacity217 = 1.0;
        if(hotspotopacity217==0)$("#hotspot217", window.document).css('visibility','hidden');
        else $("#hotspot217", window.document).css('visibility','visible');
        pos2Dpoint217 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_7Shape-0", true));
	//new added end
	//
	var pos2Dpoint23 = [];
        var norm3Dpoint23 = scene.getObjectNormal("Hotspott_7Shape-0");
        var hotspotopacity23 = infinityrt_dp(norm3Dpoint23, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity23>0 && (hotspotOn == true )) hotspotopacity23=0;
        if (hotspotopacity23 < 0.0) hotspotopacity23 = 0.0;
        else if (hotspotopacity23 > 1.0) hotspotopacity23 = 1.0;
        if(hotspotopacity23==0)$("#hotspot23", window.document).css('visibility','hidden');
        else $("#hotspot23", window.document).css('visibility','visible');
        pos2Dpoint23 = scene.projectPoint(scene.getObjectLocation("Hotspott_7Shape-0", true));
	
	var pos2Dpoint24 = [];
        var norm3Dpoint24 = scene.getObjectNormal("Hotspott_8Shape-0");
        var hotspotopacity24 = infinityrt_dp(norm3Dpoint24, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity24>0 && (hotspotOn == true )) hotspotopacity24=0;
        if (hotspotopacity24 < 0.0) hotspotopacity24 = 0.0;
        else if (hotspotopacity24 > 1.0) hotspotopacity24 = 1.0;
        if(hotspotopacity24==0)$("#hotspot24", window.document).css('visibility','hidden');
        else $("#hotspot24", window.document).css('visibility','visible');
        pos2Dpoint24 = scene.projectPoint(scene.getObjectLocation("Hotspott_8Shape-0", true));
	
	var pos2Dpoint25 = [];
        var norm3Dpoint25 = scene.getObjectNormal("Hotspott_9Shape-0");
        var hotspotopacity25 = infinityrt_dp(norm3Dpoint25, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity25>0 && (hotspotOn == true )) hotspotopacity25=0;
        if (hotspotopacity25 < 0.0) hotspotopacity25 = 0.0;
        else if (hotspotopacity25 > 1.0) hotspotopacity25 = 1.0;
        if(hotspotopacity25==0)$("#hotspot25", window.document).css('visibility','hidden');
        else $("#hotspot25", window.document).css('visibility','visible');
        pos2Dpoint25 = scene.projectPoint(scene.getObjectLocation("Hotspott_9Shape-0", true));
	
	var pos2Dpoint26 = [];
        var norm3Dpoint26 = scene.getObjectNormal("Hotspott_10Shape-0");
        var hotspotopacity26 = infinityrt_dp(norm3Dpoint26, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity26>0 && (hotspotOn == true )) hotspotopacity26=0;
        if (hotspotopacity26 < 0.0) hotspotopacity26 = 0.0;
        else if (hotspotopacity26 > 1.0) hotspotopacity26 = 1.0;
        if(hotspotopacity26==0)$("#hotspot26", window.document).css('visibility','hidden');
        else $("#hotspot26", window.document).css('visibility','visible');
        pos2Dpoint26 = scene.projectPoint(scene.getObjectLocation("Hotspott_10Shape-0", true));
	
	var pos2Dpoint27 = [];
        var norm3Dpoint27 = scene.getObjectNormal("Hotspott_11Shape-0");
        var hotspotopacity27 = infinityrt_dp(norm3Dpoint27, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity27>0 && (hotspotOn == true )) hotspotopacity27=0;
        if (hotspotopacity27 < 0.0) hotspotopacity27 = 0.0;
        else if (hotspotopacity27 > 1.0) hotspotopacity27 = 1.0;
        if(hotspotopacity27==0)$("#hotspot27", window.document).css('visibility','hidden');
        else $("#hotspot27", window.document).css('visibility','visible');
        pos2Dpoint27 = scene.projectPoint(scene.getObjectLocation("Hotspott_11Shape-0", true));
	
	var pos2Dpoint28 = [];
        var norm3Dpoint28 = scene.getObjectNormal("Hotspott_12Shape-0");
        var hotspotopacity28 = infinityrt_dp(norm3Dpoint28, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity28>0 && (hotspotOn == true )) hotspotopacity28=0;
        if (hotspotopacity28 < 0.0) hotspotopacity28 = 0.0;
        else if (hotspotopacity28 > 1.0) hotspotopacity28 = 1.0;
        if(hotspotopacity28==0)$("#hotspot28", window.document).css('visibility','hidden');
        else $("#hotspot28", window.document).css('visibility','visible');
        pos2Dpoint28 = scene.projectPoint(scene.getObjectLocation("Hotspott_12Shape-0", true));
	
	var pos2Dpoint29 = [];
        var norm3Dpoint29 = scene.getObjectNormal("Hotspott_13Shape-0");
        var hotspotopacity29 = infinityrt_dp(norm3Dpoint29, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity29>0 && (hotspotOn == true )) hotspotopacity29=0;
        if (hotspotopacity29 < 0.0) hotspotopacity29 = 0.0;
        else if (hotspotopacity29 > 1.0) hotspotopacity29 = 1.0;
        if(hotspotopacity29==0)$("#hotspot29", window.document).css('visibility','hidden');
        else $("#hotspot29", window.document).css('visibility','visible');
        pos2Dpoint29 = scene.projectPoint(scene.getObjectLocation("Hotspott_13Shape-0", true));
	
	var pos2Dpoint30 = [];
        var norm3Dpoint30 = scene.getObjectNormal("Hotspott_14Shape-0");
        var hotspotopacity30 = infinityrt_dp(norm3Dpoint30, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity30>0 && (hotspotOn == true )) hotspotopacity30=0;
        if (hotspotopacity30 < 0.0) hotspotopacity30 = 0.0;
        else if (hotspotopacity30 > 1.0) hotspotopacity30 = 1.0;
        if(hotspotopacity30==0)$("#hotspot30", window.document).css('visibility','hidden');
        else $("#hotspot30", window.document).css('visibility','visible');
        pos2Dpoint30 = scene.projectPoint(scene.getObjectLocation("Hotspott_14Shape-0", true));
	
	var pos2Dpoint31 = [];
        var norm3Dpoint31 = scene.getObjectNormal("Hotspott_15Shape-0");
        var hotspotopacity31 = infinityrt_dp(norm3Dpoint31, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity31>0 && (hotspotOn == true )) hotspotopacity31=0;
        if (hotspotopacity31 < 0.0) hotspotopacity31 = 0.0;
        else if (hotspotopacity31 > 1.0) hotspotopacity31 = 1.0;
        if(hotspotopacity31==0)$("#hotspot31", window.document).css('visibility','hidden');
        else $("#hotspot31", window.document).css('visibility','visible');
        pos2Dpoint31 = scene.projectPoint(scene.getObjectLocation("Hotspott_15Shape-0", true));
	
	var pos2Dpoint32 = [];
        var norm3Dpoint32 = scene.getObjectNormal("Hotspott_16Shape-0");
        var hotspotopacity32 = infinityrt_dp(norm3Dpoint32, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity32>0 && (hotspotOn == true )) hotspotopacity32=0;
        if (hotspotopacity32 < 0.0) hotspotopacity32 = 0.0;
        else if (hotspotopacity32 > 1.0) hotspotopacity32 = 1.0;
        if(hotspotopacity32==0)$("#hotspot32", window.document).css('visibility','hidden');
        else $("#hotspot32", window.document).css('visibility','visible');
        pos2Dpoint32 = scene.projectPoint(scene.getObjectLocation("Hotspott_16Shape-0", true));
	
	var pos2Dpoint33 = [];
        var norm3Dpoint33 = scene.getObjectNormal("Hotspott_17Shape-0");
        var hotspotopacity33 = infinityrt_dp(norm3Dpoint33, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity33>0 && (hotspotOn == true )) hotspotopacity33=0;
        if (hotspotopacity33 < 0.0) hotspotopacity33 = 0.0;
        else if (hotspotopacity33 > 1.0) hotspotopacity33 = 1.0;
        if(hotspotopacity33==0)$("#hotspot33", window.document).css('visibility','hidden');
        else $("#hotspot33", window.document).css('visibility','visible');
        pos2Dpoint33 = scene.projectPoint(scene.getObjectLocation("Hotspott_17Shape-0", true));
	
	//new added 7
	var pos2Dpoint411 = [];
        var norm3Dpoint411 = scene.getObjectNormal("new_Hotspott_1Shape-0");
        var hotspotopacity411 = infinityrt_dp(norm3Dpoint411, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity411>0 && (hotspotOn == true )) hotspotopacity411=0;
        if (hotspotopacity411 < 0.0) hotspotopacity411 = 0.0;
        else if (hotspotopacity411 > 1.0) hotspotopacity411 = 1.0;
        if(hotspotopacity411==0)$("#hotspot411", window.document).css('visibility','hidden');
        else $("#hotspot411", window.document).css('visibility','visible');
        pos2Dpoint411 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_1Shape-0", true));
	
	var pos2Dpoint412 = [];
        var norm3Dpoint412 = scene.getObjectNormal("new_Hotspott_2Shape-0");
        var hotspotopacity412 = infinityrt_dp(norm3Dpoint412, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity412>0 && (hotspotOn == true )) hotspotopacity412=0;
        if (hotspotopacity412 < 0.0) hotspotopacity412 = 0.0;
        else if (hotspotopacity412 > 1.0) hotspotopacity412 = 1.0;
        if(hotspotopacity412==0)$("#hotspot412", window.document).css('visibility','hidden');
        else $("#hotspot412", window.document).css('visibility','visible');
        pos2Dpoint412 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_2Shape-0", true));
	
	var pos2Dpoint413 = [];
        var norm3Dpoint413 = scene.getObjectNormal("new_Hotspott_3Shape-0");
        var hotspotopacity413 = infinityrt_dp(norm3Dpoint413, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity413>0 && (hotspotOn == true )) hotspotopacity413=0;
        if (hotspotopacity413 < 0.0) hotspotopacity413 = 0.0;
        else if (hotspotopacity413 > 1.0) hotspotopacity413 = 1.0;
        if(hotspotopacity413==0)$("#hotspot413", window.document).css('visibility','hidden');
        else $("#hotspot413", window.document).css('visibility','visible');
        pos2Dpoint413 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_3Shape-0", true));
	
	var pos2Dpoint414 = [];
        var norm3Dpoint414 = scene.getObjectNormal("new_Hotspott_4Shape-0");
        var hotspotopacity414 = infinityrt_dp(norm3Dpoint414, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity414>0 && (hotspotOn == true )) hotspotopacity414=0;
        if (hotspotopacity414 < 0.0) hotspotopacity414 = 0.0;
        else if (hotspotopacity414 > 1.0) hotspotopacity414 = 1.0;
        if(hotspotopacity414==0)$("#hotspot414", window.document).css('visibility','hidden');
        else $("#hotspot414", window.document).css('visibility','visible');
        pos2Dpoint414 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_4Shape-0", true));
	
	var pos2Dpoint415 = [];
        var norm3Dpoint415 = scene.getObjectNormal("new_Hotspott_5Shape-0");
        var hotspotopacity415 = infinityrt_dp(norm3Dpoint415, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity415>0 && (hotspotOn == true )) hotspotopacity415=0;
        if (hotspotopacity415 < 0.0) hotspotopacity415 = 0.0;
        else if (hotspotopacity415 > 1.0) hotspotopacity415 = 1.0;
        if(hotspotopacity415==0)$("#hotspot415", window.document).css('visibility','hidden');
        else $("#hotspot415", window.document).css('visibility','visible');
        pos2Dpoint415 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_5Shape-0", true));
	
	var pos2Dpoint416 = [];
        var norm3Dpoint416 = scene.getObjectNormal("new_Hotspott_6Shape-0");
        var hotspotopacity416 = infinityrt_dp(norm3Dpoint416, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity416>0 && (hotspotOn == true )) hotspotopacity416=0;
        if (hotspotopacity416 < 0.0) hotspotopacity416 = 0.0;
        else if (hotspotopacity416 > 1.0) hotspotopacity416 = 1.0;
        if(hotspotopacity416==0)$("#hotspot416", window.document).css('visibility','hidden');
        else $("#hotspot416", window.document).css('visibility','visible');
        pos2Dpoint416 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_6Shape-0", true));
	
	var pos2Dpoint417 = [];
        var norm3Dpoint417 = scene.getObjectNormal("new_Hotspott_7Shape-0");
        var hotspotopacity417 = infinityrt_dp(norm3Dpoint417, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity417>0 && (hotspotOn == true )) hotspotopacity417=0;
        if (hotspotopacity417 < 0.0) hotspotopacity417 = 0.0;
        else if (hotspotopacity417 > 1.0) hotspotopacity417 = 1.0;
        if(hotspotopacity417==0)$("#hotspot417", window.document).css('visibility','hidden');
        else $("#hotspot417", window.document).css('visibility','visible');
        pos2Dpoint417 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_7Shape-0", true));
	//new added end
	
	
	
	
	//
	var pos2Dpoint34 = [];
        var norm3Dpoint34 = scene.getObjectNormal("Hotspott_18Shape-0");
        var hotspotopacity34 = infinityrt_dp(norm3Dpoint34, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity34>0 && (hotspotOn == true )) hotspotopacity34=0;
        if (hotspotopacity34 < 0.0) hotspotopacity34 = 0.0;
        else if (hotspotopacity34 > 1.0) hotspotopacity34 = 1.0;
        if(hotspotopacity34==0)$("#hotspot34", window.document).css('visibility','hidden');
        else $("#hotspot34", window.document).css('visibility','visible');
        pos2Dpoint34 = scene.projectPoint(scene.getObjectLocation("Hotspott_18Shape-0", true));
	
	var pos2Dpoint35 = [];
        var norm3Dpoint35 = scene.getObjectNormal("Hotspott_19Shape-0");
        var hotspotopacity35 = infinityrt_dp(norm3Dpoint35, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity35>0 && (hotspotOn == true )) hotspotopacity35=0;
        if (hotspotopacity35 < 0.0) hotspotopacity35 = 0.0;
        else if (hotspotopacity35 > 1.0) hotspotopacity35 = 1.0;
        if(hotspotopacity35==0)$("#hotspot35", window.document).css('visibility','hidden');
        else $("#hotspot35", window.document).css('visibility','visible');
        pos2Dpoint35 = scene.projectPoint(scene.getObjectLocation("Hotspott_19Shape-0", true));
	
	var pos2Dpoint36 = [];
        var norm3Dpoint36 = scene.getObjectNormal("Hotspott_20Shape-0");
        var hotspotopacity36 = infinityrt_dp(norm3Dpoint36, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity36>0 && (hotspotOn == true )) hotspotopacity36=0;
        if (hotspotopacity36 < 0.0) hotspotopacity36 = 0.0;
        else if (hotspotopacity36 > 1.0) hotspotopacity36 = 1.0;
        if(hotspotopacity36==0)$("#hotspot36", window.document).css('visibility','hidden');
        else $("#hotspot36", window.document).css('visibility','visible');
        pos2Dpoint36 = scene.projectPoint(scene.getObjectLocation("Hotspott_20Shape-0", true));
	
	var pos2Dpoint37 = [];
        var norm3Dpoint37 = scene.getObjectNormal("Hotspott_21Shape-0");
        var hotspotopacity37 = infinityrt_dp(norm3Dpoint37, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity37>0 && (hotspotOn == true )) hotspotopacity37=0;
        if (hotspotopacity37 < 0.0) hotspotopacity37 = 0.0;
        else if (hotspotopacity37 > 1.0) hotspotopacity37 = 1.0;
        if(hotspotopacity37==0)$("#hotspot37", window.document).css('visibility','hidden');
        else $("#hotspot37", window.document).css('visibility','visible');
        pos2Dpoint37 = scene.projectPoint(scene.getObjectLocation("Hotspott_21Shape-0", true));
	
	var pos2Dpoint38 = [];
        var norm3Dpoint38 = scene.getObjectNormal("Hotspott_22Shape-0");
        var hotspotopacity38 = infinityrt_dp(norm3Dpoint38, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity38>0 && (hotspotOn == true )) hotspotopacity38=0;
        if (hotspotopacity38 < 0.0) hotspotopacity38 = 0.0;
        else if (hotspotopacity38 > 1.0) hotspotopacity38 = 1.0;
        if(hotspotopacity38==0)$("#hotspot38", window.document).css('visibility','hidden');
        else $("#hotspot38", window.document).css('visibility','visible');
        pos2Dpoint38 = scene.projectPoint(scene.getObjectLocation("Hotspott_22Shape-0", true));
	
	var pos2Dpoint39 = [];
        var norm3Dpoint39 = scene.getObjectNormal("Hotspott_23Shape-0");
        var hotspotopacity39 = infinityrt_dp(norm3Dpoint39, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity39>0 && (hotspotOn == true )) hotspotopacity39=0;
        if (hotspotopacity39 < 0.0) hotspotopacity39 = 0.0;
        else if (hotspotopacity39 > 1.0) hotspotopacity39 = 1.0;
        if(hotspotopacity39==0)$("#hotspot39", window.document).css('visibility','hidden');
        else $("#hotspot39", window.document).css('visibility','visible');
        pos2Dpoint39 = scene.projectPoint(scene.getObjectLocation("Hotspott_23Shape-0", true));
	
	var pos2Dpoint40 = [];
        var norm3Dpoint40 = scene.getObjectNormal("Hotspott_24Shape-0");
        var hotspotopacity40 = infinityrt_dp(norm3Dpoint40, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity40>0 && (hotspotOn == true )) hotspotopacity40=0;
        if (hotspotopacity40 < 0.0) hotspotopacity40 = 0.0;
        else if (hotspotopacity40 > 1.0) hotspotopacity40 = 1.0;
        if(hotspotopacity40==0)$("#hotspot40", window.document).css('visibility','hidden');
        else $("#hotspot40", window.document).css('visibility','visible');
        pos2Dpoint40 = scene.projectPoint(scene.getObjectLocation("Hotspott_24Shape-0", true));
	
	var pos2Dpoint41 = [];
        var norm3Dpoint41 = scene.getObjectNormal("Hotspott_25Shape-0");
        var hotspotopacity41 = infinityrt_dp(norm3Dpoint41, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity41>0 && (hotspotOn == true )) hotspotopacity41=0;
        if (hotspotopacity41 < 0.0) hotspotopacity41 = 0.0;
        else if (hotspotopacity41 > 1.0) hotspotopacity41 = 1.0;
        if(hotspotopacity41==0)$("#hotspot41", window.document).css('visibility','hidden');
        else $("#hotspot41", window.document).css('visibility','visible');
        pos2Dpoint41 = scene.projectPoint(scene.getObjectLocation("Hotspott_25Shape-0", true));
	
	var pos2Dpoint42 = [];
        var norm3Dpoint42 = scene.getObjectNormal("Hotspott_26Shape-0");
        var hotspotopacity42 = infinityrt_dp(norm3Dpoint42, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity42>0 && (hotspotOn == true )) hotspotopacity42=0;
        if (hotspotopacity42 < 0.0) hotspotopacity42 = 0.0;
        else if (hotspotopacity42 > 1.0) hotspotopacity42 = 1.0;
        if(hotspotopacity42==0)$("#hotspot42", window.document).css('visibility','hidden');
        else $("#hotspot42", window.document).css('visibility','visible');
        pos2Dpoint42 = scene.projectPoint(scene.getObjectLocation("Hotspott_26Shape-0", true));
	
	var pos2Dpoint43 = [];
        var norm3Dpoint43 = scene.getObjectNormal("Hotspott_27Shape-0");
        var hotspotopacity43 = infinityrt_dp(norm3Dpoint43, viewCameraZV) * hotspotopacityspeed-2.96;
        if(hotspotopacity43>0 && (hotspotOn == true )) hotspotopacity43=0;
        if (hotspotopacity43 < 0.0) hotspotopacity43 = 0.0;
        else if (hotspotopacity43 > 1.0) hotspotopacity43 = 1.0;
        if(hotspotopacity43==0)$("#hotspot43", window.document).css('visibility','hidden');
        else $("#hotspot43", window.document).css('visibility','visible');
        pos2Dpoint43 = scene.projectPoint(scene.getObjectLocation("Hotspott_27Shape-0", true));
	
	//new added 7
	var pos2Dpoint311 = [];
        var norm3Dpoint311 = scene.getObjectNormal("new_Hotspott_1Shape-0");
        var hotspotopacity311 = infinityrt_dp(norm3Dpoint311, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity311>0 && (hotspotOn == true )) hotspotopacity311=0;
        if (hotspotopacity311 < 0.0) hotspotopacity311 = 0.0;
        else if (hotspotopacity311 > 1.0) hotspotopacity311 = 1.0;
        if(hotspotopacity311==0)$("#hotspot311", window.document).css('visibility','hidden');
        else $("#hotspot311", window.document).css('visibility','visible');
        pos2Dpoint311 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_1Shape-0", true));
	
	var pos2Dpoint312 = [];
        var norm3Dpoint312 = scene.getObjectNormal("new_Hotspott_2Shape-0");
        var hotspotopacity312 = infinityrt_dp(norm3Dpoint312, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity312>0 && (hotspotOn == true )) hotspotopacity312=0;
        if (hotspotopacity312 < 0.0) hotspotopacity312 = 0.0;
        else if (hotspotopacity312 > 1.0) hotspotopacity312 = 1.0;
        if(hotspotopacity312==0)$("#hotspot312", window.document).css('visibility','hidden');
        else $("#hotspot312", window.document).css('visibility','visible');
        pos2Dpoint312 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_2Shape-0", true));
	
	var pos2Dpoint313 = [];
        var norm3Dpoint313 = scene.getObjectNormal("new_Hotspott_3Shape-0");
        var hotspotopacity313 = infinityrt_dp(norm3Dpoint313, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity313>0 && (hotspotOn == true )) hotspotopacity313=0;
        if (hotspotopacity313 < 0.0) hotspotopacity313 = 0.0;
        else if (hotspotopacity313 > 1.0) hotspotopacity313 = 1.0;
        if(hotspotopacity313==0)$("#hotspot313", window.document).css('visibility','hidden');
        else $("#hotspot313", window.document).css('visibility','visible');
        pos2Dpoint313 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_3Shape-0", true));
	
	var pos2Dpoint314 = [];
        var norm3Dpoint314 = scene.getObjectNormal("new_Hotspott_4Shape-0");
        var hotspotopacity314 = infinityrt_dp(norm3Dpoint314, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity314>0 && (hotspotOn == true )) hotspotopacity314=0;
        if (hotspotopacity314 < 0.0) hotspotopacity314 = 0.0;
        else if (hotspotopacity314 > 1.0) hotspotopacity314 = 1.0;
        if(hotspotopacity314==0)$("#hotspot314", window.document).css('visibility','hidden');
        else $("#hotspot314", window.document).css('visibility','visible');
        pos2Dpoint314 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_4Shape-0", true));
	
	var pos2Dpoint315 = [];
        var norm3Dpoint315 = scene.getObjectNormal("new_Hotspott_5Shape-0");
        var hotspotopacity315 = infinityrt_dp(norm3Dpoint315, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity315>0 && (hotspotOn == true )) hotspotopacity315=0;
        if (hotspotopacity315 < 0.0) hotspotopacity315 = 0.0;
        else if (hotspotopacity315 > 1.0) hotspotopacity315 = 1.0;
        if(hotspotopacity315==0)$("#hotspot315", window.document).css('visibility','hidden');
        else $("#hotspot315", window.document).css('visibility','visible');
        pos2Dpoint315 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_5Shape-0", true));
	
	var pos2Dpoint316 = [];
        var norm3Dpoint316 = scene.getObjectNormal("new_Hotspott_6Shape-0");
        var hotspotopacity316 = infinityrt_dp(norm3Dpoint316, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity316>0 && (hotspotOn == true )) hotspotopacity316=0;
        if (hotspotopacity316 < 0.0) hotspotopacity316 = 0.0;
        else if (hotspotopacity316 > 1.0) hotspotopacity316 = 1.0;
        if(hotspotopacity316==0)$("#hotspot316", window.document).css('visibility','hidden');
        else $("#hotspot316", window.document).css('visibility','visible');
        pos2Dpoint316 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_6Shape-0", true));
	
	var pos2Dpoint317 = [];
        var norm3Dpoint317 = scene.getObjectNormal("new_Hotspott_7Shape-0");
        var hotspotopacity317 = infinityrt_dp(norm3Dpoint317, viewCameraZV) * hotspotopacityspeed-3.08;
        if(hotspotopacity317>0 && (hotspotOn == true )) hotspotopacity317=0;
        if (hotspotopacity317 < 0.0) hotspotopacity317 = 0.0;
        else if (hotspotopacity317 > 1.0) hotspotopacity317 = 1.0;
        if(hotspotopacity317==0)$("#hotspot317", window.document).css('visibility','hidden');
        else $("#hotspot317", window.document).css('visibility','visible');
        pos2Dpoint317 = scene.projectPoint(scene.getObjectLocation("new_Hotspott_7Shape-0", true));
	//new added end


	   var leftPosPoint1 = (pos2Dpoint1[0] * 50) + 49;
	   var leftPosPoint2 = (pos2Dpoint2[0] * 50) + 50;
	   var leftPosPoint3 = (pos2Dpoint3[0] * 50) + 50;
	   var leftPosPoint4 = (pos2Dpoint4[0] * 50) + 50;
	   var leftPosPoint5 = (pos2Dpoint5[0] * 50) + 50;
	   var leftPosPoint6 = (pos2Dpoint6[0] * 50) + 50;
	   var leftPosPoint7 = (pos2Dpoint7[0] * 50) + 50;
	   var leftPosPoint8 = (pos2Dpoint8[0] * 50) + 50;
	   var leftPosPoint9 = (pos2Dpoint9[0] * 50) + 50;
	   var leftPosPoint10 = (pos2Dpoint10[0] * 50) + 50;
	   var leftPosPoint11 = (pos2Dpoint11[0] * 50) + 50;
	var leftPosPoint111 = (pos2Dpoint111[0] * 50) + 50;
	   var leftPosPoint12 = (pos2Dpoint12[0] * 50) + 50;
	   var leftPosPoint13 = (pos2Dpoint13[0] * 50) + 50;
	   var leftPosPoint14 = (pos2Dpoint14[0] * 50) + 50;
	   var leftPosPoint15 = (pos2Dpoint15[0] * 50) + 50;
       var leftPosPoint16 = (pos2Dpoint16[0] * 50) + 50;
	var leftPosPoint114 = (pos2Dpoint114[0] * 50) + 50;
	   var leftPosPoint17 = (pos2Dpoint17[0] * 50) + 50; 	
	   var leftPosPoint18 = (pos2Dpoint18[0] * 50) + 50; 	
	   var leftPosPoint19 = (pos2Dpoint19[0] * 50) + 50; 	
	   var leftPosPoint20 = (pos2Dpoint20[0] * 50) + 50; 	
	   var leftPosPoint21 = (pos2Dpoint21[0] * 50) + 50; 	
	   var leftPosPoint22 = (pos2Dpoint22[0] * 50) + 50; 	
	   var leftPosPoint23 = (pos2Dpoint23[0] * 50) + 50; 	
	   var leftPosPoint24 = (pos2Dpoint24[0] * 50) + 50; 	
	   var leftPosPoint25 = (pos2Dpoint25[0] * 50) + 50; 	
	   var leftPosPoint26 = (pos2Dpoint26[0] * 50) + 50; 	
	   var leftPosPoint27 = (pos2Dpoint27[0] * 50) + 50; 	
	   var leftPosPoint28 = (pos2Dpoint28[0] * 50) + 50; 	
	   var leftPosPoint29 = (pos2Dpoint29[0] * 50) + 50; 	
	   var leftPosPoint30 = (pos2Dpoint30[0] * 50) + 50; 	
	   var leftPosPoint31 = (pos2Dpoint31[0] * 50) + 50; 	
	   var leftPosPoint32 = (pos2Dpoint32[0] * 50) + 50; 	
	   var leftPosPoint33 = (pos2Dpoint33[0] * 50) + 50; 	
	   var leftPosPoint34 = (pos2Dpoint34[0] * 50) + 50; 	
	   var leftPosPoint35 = (pos2Dpoint35[0] * 50) + 50; 	
	   var leftPosPoint36 = (pos2Dpoint36[0] * 50) + 50; 	
	   var leftPosPoint37 = (pos2Dpoint37[0] * 50) + 50; 	
	   var leftPosPoint38 = (pos2Dpoint38[0] * 50) + 50; 	
	   var leftPosPoint39 = (pos2Dpoint39[0] * 50) + 50; 	
	   var leftPosPoint40 = (pos2Dpoint40[0] * 50) + 50; 	
	   var leftPosPoint41 = (pos2Dpoint41[0] * 50) + 50; 	
	   var leftPosPoint42 = (pos2Dpoint42[0] * 50) + 50; 	
	   var leftPosPoint43 = (pos2Dpoint43[0] * 50) + 50; 
	   var leftPosPoint211 = (pos2Dpoint211[0] * 50) + 50; 	
	   var leftPosPoint212 = (pos2Dpoint212[0] * 50) + 50; 	
	   var leftPosPoint213 = (pos2Dpoint213[0] * 50) + 50; 	
	   var leftPosPoint214 = (pos2Dpoint214[0] * 50) + 50; 	
	   var leftPosPoint215 = (pos2Dpoint215[0] * 50) + 50; 	
	   var leftPosPoint216 = (pos2Dpoint216[0] * 50) + 50; 	
	   var leftPosPoint217 = (pos2Dpoint217[0] * 50) + 50; 	
	   var leftPosPoint311 = (pos2Dpoint311[0] * 50) + 50; 	
	   var leftPosPoint312 = (pos2Dpoint312[0] * 50) + 50; 	
	   var leftPosPoint313 = (pos2Dpoint313[0] * 50) + 50; 	
	   var leftPosPoint314 = (pos2Dpoint314[0] * 50) + 50; 	
	   var leftPosPoint315 = (pos2Dpoint315[0] * 50) + 50; 	
	   var leftPosPoint316 = (pos2Dpoint316[0] * 50) + 50; 	
	   var leftPosPoint317 = (pos2Dpoint317[0] * 50) + 50;
	   var leftPosPoint411 = (pos2Dpoint411[0] * 50) + 50; 	
	   var leftPosPoint412 = (pos2Dpoint412[0] * 50) + 50; 	
	   var leftPosPoint413 = (pos2Dpoint413[0] * 50) + 50; 	
	   var leftPosPoint414 = (pos2Dpoint414[0] * 50) + 50; 	
	   var leftPosPoint415 = (pos2Dpoint415[0] * 50) + 50; 	
	   var leftPosPoint416 = (pos2Dpoint416[0] * 50) + 50; 	
	   var leftPosPoint417 = (pos2Dpoint417[0] * 50) + 50; 	
    	   
       var toptPosPoint1 = -((pos2Dpoint1[1] * 50) - 50);
	   var toptPosPoint2 = -((pos2Dpoint2[1] * 50) - 50);
	   var toptPosPoint3 = -((pos2Dpoint3[1] * 50) - 50);
	   var toptPosPoint4 = -((pos2Dpoint4[1] * 50) - 50);
	   var toptPosPoint5 = -((pos2Dpoint5[1] * 50) - 50);
	   var toptPosPoint6 = -((pos2Dpoint6[1] * 50) - 50);
	   var toptPosPoint7 = -((pos2Dpoint7[1] * 50) - 50);
	   var toptPosPoint8 = -((pos2Dpoint8[1] * 50) - 50);
	   var toptPosPoint9 = -((pos2Dpoint9[1] * 50) - 50);
	   var toptPosPoint10 = -((pos2Dpoint10[1] * 50) - 50);
	   var toptPosPoint11 = -((pos2Dpoint11[1] * 50) -50);
	var toptPosPoint111 = -((pos2Dpoint111[1] * 50) -50);
       var toptPosPoint12 = -((pos2Dpoint12[1] * 50) - 50);
	   var toptPosPoint13 = -((pos2Dpoint13[1] * 50) - 50);
	   var toptPosPoint14 = -((pos2Dpoint14[1] * 50) - 50);
	   var toptPosPoint15 = -((pos2Dpoint15[1] * 50) - 50);
       var toptPosPoint16 = -((pos2Dpoint16[1] * 50) - 50);
	var toptPosPoint114 = -((pos2Dpoint114[1] * 50) - 50);
	   var toptPosPoint17 = -((pos2Dpoint17[1] * 50) - 50);
	   var toptPosPoint18 = -((pos2Dpoint18[1] * 50) - 50);
	   var toptPosPoint19 = -((pos2Dpoint19[1] * 50) - 50);
	   var toptPosPoint20 = -((pos2Dpoint20[1] * 50) - 50);
	   var toptPosPoint21 = -((pos2Dpoint21[1] * 50) - 50);
	   var toptPosPoint22 = -((pos2Dpoint22[1] * 50) - 50);
	   var toptPosPoint23 = -((pos2Dpoint23[1] * 50) - 50);
	   var toptPosPoint24 = -((pos2Dpoint24[1] * 50) - 50);
	   var toptPosPoint25 = -((pos2Dpoint25[1] * 50) - 50);
	   var toptPosPoint26 = -((pos2Dpoint26[1] * 50) - 50);
	   var toptPosPoint27 = -((pos2Dpoint27[1] * 50) - 50);
	   var toptPosPoint28 = -((pos2Dpoint28[1] * 50) - 50);
	   var toptPosPoint29 = -((pos2Dpoint29[1] * 50) - 50);
	   var toptPosPoint30 = -((pos2Dpoint30[1] * 50) - 50);
	   var toptPosPoint31 = -((pos2Dpoint31[1] * 50) - 50);
	   var toptPosPoint32 = -((pos2Dpoint32[1] * 50) - 50);
	   var toptPosPoint33 = -((pos2Dpoint33[1] * 50) - 50);
	   var toptPosPoint34 = -((pos2Dpoint34[1] * 50) - 50);
	   var toptPosPoint35 = -((pos2Dpoint35[1] * 50) - 50);
	   var toptPosPoint36 = -((pos2Dpoint36[1] * 50) - 50);
	   var toptPosPoint37 = -((pos2Dpoint37[1] * 50) - 50);
	   var toptPosPoint38 = -((pos2Dpoint38[1] * 50) - 50);
	   var toptPosPoint39 = -((pos2Dpoint39[1] * 50) - 50);
	   var toptPosPoint40 = -((pos2Dpoint40[1] * 50) - 50);
	   var toptPosPoint41 = -((pos2Dpoint41[1] * 50) - 50);
	   var toptPosPoint42 = -((pos2Dpoint42[1] * 50) - 50);
	   var toptPosPoint43 = -((pos2Dpoint43[1] * 50) - 50);
	   var toptPosPoint211 = -((pos2Dpoint211[1] * 50) - 50);
	   var toptPosPoint212 = -((pos2Dpoint212[1] * 50) - 50);
	   var toptPosPoint213 = -((pos2Dpoint213[1] * 50) - 50);
	   var toptPosPoint214 = -((pos2Dpoint214[1] * 50) - 50);
	   var toptPosPoint215 = -((pos2Dpoint215[1] * 50) - 50);
	   var toptPosPoint216 = -((pos2Dpoint216[1] * 50) - 50);
	   var toptPosPoint217 = -((pos2Dpoint217[1] * 50) - 50);
	   var toptPosPoint311 = -((pos2Dpoint311[1] * 50) - 50);
	   var toptPosPoint312 = -((pos2Dpoint312[1] * 50) - 50);
	   var toptPosPoint313 = -((pos2Dpoint313[1] * 50) - 50);
	   var toptPosPoint314 = -((pos2Dpoint314[1] * 50) - 50);
	   var toptPosPoint315 = -((pos2Dpoint315[1] * 50) - 50);
	   var toptPosPoint316 = -((pos2Dpoint316[1] * 50) - 50);
	   var toptPosPoint317 = -((pos2Dpoint317[1] * 50) - 50);
	   var toptPosPoint411 = -((pos2Dpoint411[1] * 50) - 50);
	   var toptPosPoint412 = -((pos2Dpoint412[1] * 50) - 50);
	   var toptPosPoint413 = -((pos2Dpoint413[1] * 50) - 50);
	   var toptPosPoint414 = -((pos2Dpoint414[1] * 50) - 50);
	   var toptPosPoint415 = -((pos2Dpoint415[1] * 50) - 50);
	   var toptPosPoint416 = -((pos2Dpoint416[1] * 50) - 50);
	   var toptPosPoint417 = -((pos2Dpoint417[1] * 50) - 50);
        

	   $("#hotspot1").css('left', leftPosPoint1 + '%').css('top', toptPosPoint1 + '%');
	   $("#hotspot2").css('left', leftPosPoint2 + '%').css('top', toptPosPoint2 + '%');
	   $("#hotspot3").css('left', leftPosPoint3 + '%').css('top', toptPosPoint3 + '%');
	   $("#hotspot4").css('left', leftPosPoint4 + '%').css('top', toptPosPoint4 + '%');
	   $("#hotspot5").css('left', leftPosPoint5 + '%').css('top', toptPosPoint5 + '%');
	   $("#hotspot6").css('left', leftPosPoint6 + '%').css('top', toptPosPoint6 + '%');
	   $("#hotspot7").css('left', leftPosPoint7 + '%').css('top', toptPosPoint7 + '%');
	   $("#hotspot8").css('left', leftPosPoint8 + '%').css('top', toptPosPoint8 + '%');
	   $("#hotspot9").css('left', leftPosPoint9 + '%').css('top', toptPosPoint9 + '%');
	   $("#hotspot10").css('left', leftPosPoint10 + '%').css('top', toptPosPoint10 + '%');
	   $("#hotspot11").css('left', leftPosPoint11 + '%').css('top', toptPosPoint11 + '%');
	$("#hotspot111").css('left', leftPosPoint111 + '%').css('top', toptPosPoint111 + '%');
       $("#hotspot12").css('left', leftPosPoint12 + '%').css('top', toptPosPoint12 + '%');
	   $("#hotspot13").css('left', leftPosPoint13 + '%').css('top', toptPosPoint13 + '%');
	   $("#hotspot14").css('left', leftPosPoint14 + '%').css('top', toptPosPoint14 + '%');
       $("#hotspot15").css('left', leftPosPoint15 + '%').css('top', toptPosPoint15 + '%');
       $("#hotspot16").css('left', leftPosPoint16 + '%').css('top', toptPosPoint16 + '%');
	$("#hotspot114").css('left', leftPosPoint114 + '%').css('top', toptPosPoint114 + '%');
	   $("#hotspot17").css('left', leftPosPoint17 + '%').css('top', toptPosPoint17 + '%');
	   $("#hotspot18").css('left', leftPosPoint18 + '%').css('top', toptPosPoint18 + '%');
	   $("#hotspot19").css('left', leftPosPoint19 + '%').css('top', toptPosPoint19 + '%');
	   $("#hotspot20").css('left', leftPosPoint20 + '%').css('top', toptPosPoint20 + '%');
	   $("#hotspot21").css('left', leftPosPoint21 + '%').css('top', toptPosPoint21 + '%');
	   $("#hotspot22").css('left', leftPosPoint22 + '%').css('top', toptPosPoint22 + '%');
	   $("#hotspot23").css('left', leftPosPoint23 + '%').css('top', toptPosPoint23 + '%');
	   $("#hotspot24").css('left', leftPosPoint24 + '%').css('top', toptPosPoint24 + '%');
	   $("#hotspot25").css('left', leftPosPoint25 + '%').css('top', toptPosPoint25 + '%');
	   $("#hotspot26").css('left', leftPosPoint26 + '%').css('top', toptPosPoint26 + '%');
	   $("#hotspot27").css('left', leftPosPoint27 + '%').css('top', toptPosPoint27 + '%');
	   $("#hotspot28").css('left', leftPosPoint28 + '%').css('top', toptPosPoint28 + '%');
	   $("#hotspot29").css('left', leftPosPoint29 + '%').css('top', toptPosPoint29 + '%');
	   $("#hotspot30").css('left', leftPosPoint30 + '%').css('top', toptPosPoint30 + '%');
	   $("#hotspot31").css('left', leftPosPoint31 + '%').css('top', toptPosPoint31 + '%');
	   $("#hotspot32").css('left', leftPosPoint32 + '%').css('top', toptPosPoint32 + '%');
	   $("#hotspot33").css('left', leftPosPoint33 + '%').css('top', toptPosPoint33 + '%');
	   $("#hotspot34").css('left', leftPosPoint34 + '%').css('top', toptPosPoint34 + '%');
	   $("#hotspot35").css('left', leftPosPoint35 + '%').css('top', toptPosPoint35 + '%');
	   $("#hotspot36").css('left', leftPosPoint36 + '%').css('top', toptPosPoint36 + '%');
	   $("#hotspot37").css('left', leftPosPoint37 + '%').css('top', toptPosPoint37 + '%');
	   $("#hotspot38").css('left', leftPosPoint38 + '%').css('top', toptPosPoint38 + '%');
	   $("#hotspot39").css('left', leftPosPoint39 + '%').css('top', toptPosPoint39 + '%');
	   $("#hotspot40").css('left', leftPosPoint40 + '%').css('top', toptPosPoint40 + '%');
	   $("#hotspot41").css('left', leftPosPoint41 + '%').css('top', toptPosPoint41 + '%');
	   $("#hotspot42").css('left', leftPosPoint42 + '%').css('top', toptPosPoint42 + '%');
	   $("#hotspot43").css('left', leftPosPoint43 + '%').css('top', toptPosPoint43 + '%');
	
	$("#hotspot211").css('left', leftPosPoint211 + '%').css('top', toptPosPoint211 + '%');
	$("#hotspot212").css('left', leftPosPoint212 + '%').css('top', toptPosPoint212 + '%');
	$("#hotspot213").css('left', leftPosPoint213 + '%').css('top', toptPosPoint213 + '%');
	$("#hotspot214").css('left', leftPosPoint214 + '%').css('top', toptPosPoint214 + '%');
	$("#hotspot215").css('left', leftPosPoint215 + '%').css('top', toptPosPoint215 + '%');
	$("#hotspot216").css('left', leftPosPoint216 + '%').css('top', toptPosPoint216 + '%');
	$("#hotspot217").css('left', leftPosPoint217 + '%').css('top', toptPosPoint217 + '%');
	
	$("#hotspot311").css('left', leftPosPoint311 + '%').css('top', toptPosPoint311 + '%');
	$("#hotspot312").css('left', leftPosPoint312 + '%').css('top', toptPosPoint312 + '%');
	$("#hotspot313").css('left', leftPosPoint313 + '%').css('top', toptPosPoint313 + '%');
	$("#hotspot314").css('left', leftPosPoint314 + '%').css('top', toptPosPoint314 + '%');
	$("#hotspot315").css('left', leftPosPoint315 + '%').css('top', toptPosPoint315 + '%');
	$("#hotspot316").css('left', leftPosPoint316 + '%').css('top', toptPosPoint316 + '%');
	$("#hotspot317").css('left', leftPosPoint317 + '%').css('top', toptPosPoint317 + '%');
	
	$("#hotspot411").css('left', leftPosPoint411 + '%').css('top', toptPosPoint411 + '%');
	$("#hotspot412").css('left', leftPosPoint412 + '%').css('top', toptPosPoint412 + '%');
	$("#hotspot413").css('left', leftPosPoint413 + '%').css('top', toptPosPoint413 + '%');
	$("#hotspot414").css('left', leftPosPoint414 + '%').css('top', toptPosPoint414 + '%');
	$("#hotspot415").css('left', leftPosPoint415 + '%').css('top', toptPosPoint415 + '%');
	$("#hotspot416").css('left', leftPosPoint416 + '%').css('top', toptPosPoint416 + '%');
	$("#hotspot417").css('left', leftPosPoint417 + '%').css('top', toptPosPoint417 + '%');
	
	
	
	   if(Math.floor(sceneViewMatrix[5])==0){
				clockWise=false;
	 	 }else if(Math.floor(sceneViewMatrix[5])==-1){
				clockWise=true;
		 }
}

var mpos = [0, 0];
var mdown = false;
var panNav = false;
var prevAnimation = null;
function mouseDown(ev){
     if (!animStoped) return; 
     if(autoplayAnim)autoPauseAllAnimations();
        $("#rightAnim").animate({right: '-235px'}, "slow");
        rightAnimToggle = true;
    autoRotateStop();
//    topCover = false;
	scene._nav._navMode = 2;
	
    $("#onloadCopy").css("opacity","0");
	scene.instanceSet("HDD_12", "visible", true);
	scene.instanceSet("Body_Ref", "visible", true);
	scene.instanceSet("three_five__", "visible", true);
    mouseDownHide();
    for (var i=0; i<timeouts.length; i++) {
			clearTimeout(timeouts[i]);
		}
   
    clearTimeout(autoPlayInt)
    clearInterval(autoRotateInterval);
    clearTimeout(myVar);
    clearTimeout(startAutorot);
     for (var i=0; i<timeoutsnew.length; i++) {
			clearTimeout(timeoutsnew[i]);
		}
timeouts = [];
timeoutsnew=[];
//     	for (var j = 1; j <= 13; j++) {if(j ==5 || j ==7 || j ==9){}else{translateOut(j);}}
//     	for (var j = 1; j <= 13; j++) {if(j ==5 || j ==7 || j ==9){}else{translateOut(j);}}

//		for (var j = 1; j <= 15; j++) {if(j ==5 || j ==3 || j ==4 || j ==6 || j ==7 ||j ==8 ||j ==9 ||j ==10){}else{translateOut(j);}}  
    
         
		    var s = getScene(ev);
            if (ev.which == 3) {
              panNav = true;
             }
		    var mouseDownPos = [ev.clientX - canvas.offsetLeft, ev.clientY - canvas.offsetTop];
		    if (!s.onClick(mouseDownPos, ev.button))
		    {
			    mdown = true;
			    mpos = mouseDownPos;
			}
			reversAll();
}

function mouseUp(ev) {
    mdown = false;
    if (ev.which == 3 || panNav) panNav = false;
    handOpen();
}

function mouseOut(ev) {
    mdown = false;
    if (ev.which == 3 || panNav) panNav = false;
    handOpen();
}

	function mouseMove(ev) {        
    if (!mdown || !animStoped) return;
         if(autoplayAnim)autoPauseAllAnimations();
     for (var i=0; i<timeouts.length; i++) {
			clearTimeout(timeouts[i]);
		}
    timeouts = [];
	scene._nav._navMode = 2;
    clearInterval(autoRotateInterval);
    clearTimeout(myVar);        
    var s = getScene(ev);
    var mousePos = [ev.clientX - canvas.offsetLeft, ev.clientY - canvas.offsetTop];
    var mdelta = [(mpos[0]-mousePos[0]),(mpos[1]-mousePos[1])];
    mpos = [mousePos[0],mousePos[1]];
    //pan nav is initialized and set in ui\_ui.js for now.
     if (!panNav) {
        if (s._nav.NavRotation(mpos, mdelta)) s.clearRefine();
    } else {
        var mdelta2 = [mdelta[0] * 3, mdelta[1] * 3];
        if (s._nav.NavPan(mdelta2)) s.clearRefine();
    }
}

function mouseWheel(ev){
    if (!animStoped) return;
    if(autoplayAnim)autoPauseAllAnimations();
	scene._nav._navMode = 2;
    for (var i=0; i<timeouts.length; i++) {
			clearTimeout(timeouts[i]);
		}
timeouts = [];
    
    autoRotateStop();
    clearTimeout(autoPlayInt);
    clearInterval(autoRotateInterval);
    clearTimeout(myVar);
    autoRotateStop();
    clearTimeout(startAutorot);

//		for (var j = 1; j <= 15; j++) {translateOut(j);}
//     hideAll(); 
    if(autoplayAnim)autoPauseAllAnimations();
     reversAll();
	scene.instanceSet("HDD_12", "visible", true);
	scene.instanceSet("Body_Ref", "visible", true);
	scene.instanceSet("three_five__", "visible", true);
	 mouseDownHide();
	 mouseWheelHide();
	 $("#onloadCopy").css("opacity","0");
      var s = getScene(ev);
      var delta = ev.wheelDelta ? ev.wheelDelta : (-ev.detail * 10.0);
      //var deltaScene = (delta*0.05)*(scene.sceneRadius*0.01);
      var deltaScene = delta * 0.06;
      if (s._nav.NavChangeDolly(deltaScene))
      s.clearRefine();
}

function hideAll() {
}

function updateZoomBarBg(newval) {
    var scale = -(navMinDolly - navMaxDolly);
    var val = -newval + navMaxDolly;
    $("#zoom_slider_bg").css("height", (val / scale) * 100 + "%");
}


function updateZoomBar(newval) {
    var scale = -(navMinDolly - navMaxDolly);
    var val = -newval;
    $(".ui-slider-handle").css("bottom", (val / scale) * 100 + "%");
}

//var animStoped = true;

//function animComplete() {
////    animStoped = true;
//    g_navEnabled = true;
//}

var animStoped = true; 
var dragCursor;
var curBrowser = BrowserDetect.browser;
// IE doesn't support co-ordinates
var cursCoords = (curBrowser == "Explorer") ? "" : " 4 4";

function initDragCursor() {
    handOpen();
    $('#sliderBG').mousedown(function() {
        handClosed();
    });
    $('.ui-slider-handle').mousedown(function() {
        handClosed();
    });
    $('body').mouseup(function() {
        handOpen();
    });
    $('body').mouseup(function() {
        handOpen();
    });
}

function handClosed() {
    dragCursor = (curBrowser == "Firefox") ? "-moz-grabbing" : "url(images_gl/closedhand.cur)" + cursCoords + ", move";
    // Opera doesn't support url cursors and doesn't fall back well...
    if (curBrowser == "Opera") dragCursor = "move";
    $('.ui-slider-handle').css("cursor", dragCursor);
    $('#sliderBG').css("cursor", dragCursor);
    $('#dummy-canvas').css("cursor", dragCursor);
}

function handOpen() {
    dragCursor = (curBrowser == "Firefox") ? "-moz-grab" : "url(images_gl/openhand.cur)" + cursCoords + ", move";
    $('.ui-slider-handle').css("cursor", dragCursor);
    $('#sliderBG').css("cursor", dragCursor);
    $('#dummy-canvas').css("cursor", dragCursor);
}

var mouseIsDown = false;
var loopCtr = 0;
var touch = new Vector3();
var touches = [new Vector3(), new Vector3(), new Vector3()];
var prevTouches = [new Vector3(), new Vector3(), new Vector3()];
var prevDistance = null;
var startAutorot;
function touchStart(event) {
//     if(menu11wasclicked==true){
//		
//	} 
//	else{
//		for (var j = 1; j <= 15; j++) {if(j ==5 || j ==3 || j ==4 || j ==6 || j ==7 || j ==11 ||j ==8 ||j ==9 ||j ==10){}else{translateOut(j);}}
//	}
    
    for (var j = 1; j <= 13; j++) {if(j ==2 || j ==7){}else{translateOut(j);}}

    if(!animStoped)return;
    mdown=true;
    autoPauseAllAnimations();
    autoRotateStop();
     clearInterval(autoRotateInterval);
    clearTimeout(myVar);
    clearTimeout(startAutorot);
	reversAll();
            switch (event.touches.length) {
                case 1:
                    touches[0].set(event.touches[0].pageX, event.touches[0].pageY, 0);
                    touches[1].set(event.touches[0].pageX, event.touches[0].pageY, 0);
                    break;
                case 2:
                    for (var j = 1; j <= 15; j++) {translateOut(j);}
                    touches[0].set(event.touches[0].pageX, event.touches[0].pageY, 0);
                    touches[1].set(event.touches[1].pageX, event.touches[1].pageY, 0);
                    prevDistance = touches[0].distanceTo(touches[1]);
                    break;
            }
            prevTouches[0].copy(touches[0]);
            prevTouches[1].copy(touches[1]);
        }

var doubleTouch = false;

 function touchMove(event) {
//      if(menu11wasclicked==true){
//		
//	} 
//	else{
//		for (var j = 1; j <= 15; j++) {if(j ==5 || j ==3 || j ==4 || j ==6 || j ==7 || j ==11 ||j ==8 ||j ==9 ||j ==10){}else{translateOut(j);}}
//	}
   
     if(!animStoped || !mdown)return;
     autoPauseAllAnimations();
      for (var j = 1; j <= 13; j++) {if(j ==2 || j ==7){}else{translateOut(j);}}
     clearInterval(autoRotateInterval);
     clearTimeout(myVar);
     clearTimeout(startAutorot);
            var s = getScene(event);
            event.preventDefault();   
            event.stopPropagation();
            var getClosest = function(touch, touches) {
                var closest = touches[0];
                for (var i in touches) {
                    if (closest.distanceTo(touch) > touches[i].distanceTo(touch)) closest = touches[i];
                }
                return closest;
            }
            switch (event.touches.length) {
                case 1:
                    if (doubleTouch == false) {
                        clearInterval(autoRotateInterval);
                        clearTimeout(myVar);
                        touches[0].set(event.touches[0].pageX, event.touches[0].pageY, 0);
                        touches[1].set(event.touches[0].pageX, event.touches[0].pageY, 0);
                        if (s._nav.NavRotation([touches[0].x, touches[0].y], [(prevTouches[0].x - touches[0].x) * 1.5, (prevTouches[0].y - touches[0].y) * 1.5])) s.clearRefine();
                        //scope.rotate( touches[ 0 ].sub( getClosest( touches[ 0 ] ,prevTouches ) ).multiplyScalar( - 0.005 ) );
                    }
                    break;
                case 2:
//					$("#pointtext3").fadeOut(0);
//                    $("#pointtext6").fadeOut(0);
//                    $("#pointtext1").fadeOut(0);
                    doubleTouch = true;
                    //alert("double");
                    clearInterval(autoRotateInterval);
                    clearTimeout(myVar);
                    touches[0].set(event.touches[0].pageX, event.touches[0].pageY, 0);
                    touches[1].set(event.touches[1].pageX, event.touches[1].pageY, 0);
                    distance = touches[0].distanceTo(touches[1]);
                    var deltaScene = -(prevDistance - distance)*3;
                    if (s._nav.NavChangeDolly(deltaScene)) {
                        s.clearRefine();
                    }
                    //scope.zoom( new Vector3( 0, 0, prevDistance - distance ) );
                    prevDistance = distance;
                    var offset0 = touches[0].clone().sub(getClosest(touches[0], prevTouches));
                    var offset1 = touches[1].clone().sub(getClosest(touches[1], prevTouches));
                    offset0.x = -offset0.x;
                    offset1.x = -offset1.x;
                    var mdelta2 = [offset1.x * 10, -offset1.y * 10];
                    
                    if (s._nav.NavPan(mdelta2)) s.clearRefine();
                    //scope.pan( offset0.add( offset1 ).multiplyScalar( 0.5 ) );
                    break;
            }
            prevTouches[0].copy(touches[0]);
            prevTouches[1].copy(touches[1]);
           
        }

function touchEndCan(event) {
   mdown=false;
   setTimeout(function(){
        doubleTouch = false;
    },100);
}



function parseXml(){
//console.log("fn call in ");
 			$.ajax({
                url: 'text.xml', // name of file you want to parse
                dataType: "xml", // type of file you are trying to read
                success: function parse(document){
             $(document).find("loader").each(function(){
             	/*var loaderHeading = $(this).find('loaderHeading').text();
             	$('.loaderheading').append(loaderHeading);*/
             	var subheading = $(this).find('subheading').text();
             	$('.subheading').append(subheading);
             	var greyLeftTop = $(this).find('greyLeftTop').text();
             	$('.grey-left-top').append(greyLeftTop);
             	var greyLeftBottom = $(this).find('greyLeftBottom').text();
             	$('.grey-left-bottom').prepend(greyLeftBottom);
             	var greyRightTop = $(this).find('greyRightTop').text();
             	$('.grey-right-top').append(greyRightTop);
             	var greyRightBottom = $(this).find('greyRightBottom').text();
             	$('.grey-right-bottom').append(greyRightBottom);
             	var loaderOpen = $(this).find('loaderOpen').text();
             	$('.loader-open').append(loaderOpen);
             	var loaderZoom = $(this).find('loaderZoom').text();
             	$('.loader-zoom').append(loaderZoom);
             	var loaderRotate = $(this).find('loaderRotate').text();
             	$('.loader-rotate').append(loaderRotate);
             	var loaderMove = $(this).find('loaderMove').text();
             	$('.loader-move').append(loaderMove);
             	var leftMouse = $(this).find('leftMouse').text();
             	$('.left-mouse').prepend(leftMouse);
             	var rotateMouse = $(this).find('rotateMouse').text();
             	$('.rotate-mouse').append(rotateMouse);
             	var scrollMouse = $(this).find('scrollMouse').text();
             	$('.scroll-mouse').prepend(scrollMouse);
             	var zoomMouse = $(this).find('zoomMouse').text();
             	$('.zoom').append(zoomMouse);
             	var bothMouse = $(this).find('bothMouse').text();
             	$('.both-mouse').prepend(bothMouse);
             	var pan = $(this).find('pan').text();
             	$('.pan-mouse').append(pan);
             });   	
           
             
//             $(document).find("message").each(function(){
//             	var blackPatch = $(this).find('blackPatch').text();
//             	$('.productName span').append(blackPatch);  
//             	var cpText = $(this).find('#onloadCopy').text();
//             	$('#onloadCopy').append(cpText);
//             	var cpHeading = $(this).find('cpHeading').text();
//             	$('#cpHeading').append(cpHeading);
//                 var cpSubHeading = $(this).find('cpSubHeading').text();
//             	$('#cpSubHeading').append(cpSubHeading);
//   
//                    
//                 
//             });
                    
             $(document).find("onloadCopy").each(function(){
                var point1_1 = $(this).find('point1text1').text();
                  $('#onloadCopy p:nth-child(1)').append(point1_1);
             }); 
			
		     $(document).find("point13text").each(function(){
                var point1_1 = $(this).find('point13text1').text();
                  $('#point13text1').append(point1_1);
             });
			$(document).find("point14text").each(function(){
                var point1_1 = $(this).find('point14text1').text();
                  $('#point14text1').append(point1_1);
             });

             $(document).find("buttons").each(function(){
             	var backText = $(this).find('backText').text();
        		$('#backText').append(backText);
             	var zoomText = $(this).find('zoomText').text();
             	$('#zoomText').append(zoomText);
             	var roatateText = $(this).find('roatateText').text();
             	$('#roatateText').append(roatateText);
             	var moveText = $(this).find('moveText').text();
             	$('#moveText').append(moveText);
             	btnOpen = $(this).find('divOpen').text();
             	$('#openCloseDiv').html(btnOpen);
             	btnClose = $(this).find('divClose').text();
             	//$('#openCloseDiv').append(btnClose);
             });
             $(document).find("pointtext1").each(function(){ 
             	var point1_1 = $(this).find('point1text1').text();
             	$('#pointtext1 #Cp_text_01').append(point1_1);
                var point1_2 = $(this).find('point1text2').text();
                $('#pointtext1 #Cp_text_02').append(point1_2);
                var point1_3 = $(this).find('point1text3').text();
                $('#pointtext1 #Cp_text_03').append(point1_3);
                 var point1_4 = $(this).find('point1text4').text();
                $('#pointtext1 #Cp_text_04').append(point1_4);
                 var point1_5 = $(this).find('point1text5').text();
                $('#pointtext1 #Cp_text_05').append(point1_5);
                 var point1_6 = $(this).find('point1text6').text();
                $('#pointtext1 #Cp_text_06').append(point1_6);
                 var point1_7 = $(this).find('point1text7').text();
                $('#pointtext1 #Cp_text_07').append(point1_7);
                 var point1_8 = $(this).find('point1text8').text();
                $('#pointtext1 #Cp_text_08').append(point1_8);
                 var point1_9 = $(this).find('point1text9').text();
                $('#pointtext1 #Cp_text_09').append(point1_9);
                 var point1_10 = $(this).find('point1text10').text();
                $('#pointtext1 #Cp_text_10').append(point1_10);
                 var point1_11 = $(this).find('point1text11').text();
                $('#pointtext1 #Cp_text_11').append(point1_11);
                 var point1_12 = $(this).find('point1text12').text();
                $('#pointtext1 #Cp_text_12').append(point1_12);
                 
                  var point1_13 = $(this).find('point1text13').text();
                $('#pointtext1 .Cp_textul li:nth-child(1)').html(point1_13);
                 
                 var point1_14 = $(this).find('point1text14').text();
                $('#pointtext1 .Cp_textul li:nth-child(2)').html(point1_14);
                 
                 var point1_15 = $(this).find('point1text15').text();
                $('#pointtext1 .Cp_textul li:nth-child(3)').html(point1_15);
                 
                 var point1_16 = $(this).find('point1text16').text();
                $('#pointtext1 .Cp_textul li:nth-child(4)').html(point1_16); 
                 

             });

             $(document).find("point2text").each(function(){
							 
             });  

             $(document).find("point3text").each(function(){
                var point3_2 = $(this).find('point3text1').text();
             	$('#point3imgtxt1').append(point3_2);
                  
                var point3_3 = $(this).find('point3text2').text();
             	$('#point3imgtxt2').append(point3_3);
                  
                var point3_4 = $(this).find('point3text3').text();
             	$('#point3imgtxt3').append(point3_4);
                  
                var point3_5 = $(this).find('point3text4').text();
             	$('#point3imgtxt4').append(point3_5);
                  
                var point3_6 = $(this).find('point3text5').text();
             	$('#point3imgtxt5').append(point3_6);
				 
				var point3_7 = $(this).find('point3text6').text();
             	$('#point3imgtxt6').append(point3_7);
                 
             });
                    
            $(document).find("point4text").each(function(){
                var point4_1 = $(this).find('point4text1').text();
                $('.point4text1').append(point4_1);
                var point4_2 = $(this).find('point4text2').text();
                $('#hot1').append(point4_2); 
                var point4_3 = $(this).find('point4text3').text();
                $('#hot2').append(point4_3);  
                var point4_4 = $(this).find('point4text4').text();
                $('#hot3').append(point4_4);   
                var point4_5 = $(this).find('point4text5').text();
                $('#hot4').append(point4_5);
             });
                    
              $(document).find("point5text").each(function(){
                var point5_3 = $(this).find('point5text1').text();
             	$('#point5text li:nth-child(1)').append(point5_3);
                var point5_4 = $(this).find('point5text2').text();
             	$('#point5text li:nth-child(2)').append(point5_4);             
                var point5_5 = $(this).find('point5text3').text();
             	$('#point5text li:nth-child(3)').append(point5_5);             
                var point5_6 = $(this).find('point5text4').text();
             	$('#point5text li:nth-child(4)').append(point5_6);           
                var point5_7 = $(this).find('point5text5').text();
             	$('#point5text li:nth-child(5)').append(point5_7);           
                var point5_8 = $(this).find('point5text6').text();
             	$('#point5text li:nth-child(6)').append(point5_8);           
                var point5_9 = $(this).find('point5text7').text();
             	$('#point5text li:nth-child(7)').append(point5_9);  
                 var point5_10 = $(this).find('point5text8').text();
             	$('#hot17').append(point5_10);  
                 var point5_11 = $(this).find('point5text9').text();
             	$('#hot18').append(point5_11);  
                 var point5_12 = $(this).find('point5text10').text();
             	$('#hot19').append(point5_12); 
                 var point5_13 = $(this).find('point5text11').text();
             	$('#hot20').append(point5_13); 
                 var point5_14 = $(this).find('point5text12').text();
             	$('#hot21').append(point5_14); 
                 var point5_15 = $(this).find('point5text13').text();
             	$('#hot22').append(point5_15); 
				  
				var point5_16 = $(this).find('point5text14').text();
             	$('#hot211').append(point5_16); 
				  var point5_17 = $(this).find('point5text15').text();
             	$('#hot212').append(point5_17); 
				  var point5_18 = $(this).find('point5text16').text();
             	$('#hot213').append(point5_18); 
				  var point5_19 = $(this).find('point5text17').text();
             	$('#hot214').append(point5_19); 
				  var point5_20 = $(this).find('point5text18').text();
             	$('#hot215').append(point5_20); 
				  var point5_21 = $(this).find('point5text19').text();
             	$('#hot216').append(point5_21); 
				  var point5_22 = $(this).find('point5text20').text();
             	$('#hot217').append(point5_22); 
             });
                    
                    
                    
					
             $(document).find("pointtext6").each(function(){
                 
             	var point6_1 = $(this).find('point6text1').text();
             	$('#hot5').html(point6_1);
                 
                var point6_2 = $(this).find('point6text2').text();
             	$('#hot6').html(point6_2);
                 
                var point6_3 = $(this).find('point6text3').text();
             	$('#hot7').html(point6_3);
                 
                var point6_4 = $(this).find('point6text4').text();
             	$('#hot8').html(point6_4);
                 
                var point6_5 = $(this).find('point6text5').text();
             	$('#hot9').html(point6_5);
                 
                var point6_6 = $(this).find('point6text6').text();
             	$('#hot10').html(point6_6);
                 
                var point6_7 = $(this).find('point6text7').text();
             	$('#hot11').html(point6_7);
				 
				var point6_8 = $(this).find('point6text8').text();
             	$('#hot111').html(point6_8);
                 
            });
                    
                    
        $(document).find("point7text").each(function(){
              var point7_1 = $(this).find('point7text1').text();
             $('#point7text li:nth-child(1)').append(point7_1);
              var point7_2 = $(this).find('point7text2').text();
              $('#point7text li:nth-child(2)').append(point7_2);
              var point7_3 = $(this).find('point7text3').text();
              $('#point7text li:nth-child(3)').append(point7_3);
              var point7_4 = $(this).find('point7text4').text();
              $('#point7text li:nth-child(4)').append(point7_4);
              var point7_7 = $(this).find('point7text5').text();
              $('#point7text li:nth-child(5)').append(point7_7);
              var point7_6 = $(this).find('point7text6').text();
              $('#point7text li:nth-child(6)').append(point7_6);
              var point7_7 = $(this).find('point7text7').text();
              $('#point7text li:nth-child(7)').append(point7_7);
              var point7_8 = $(this).find('point7text8').text();
              $('#hot23').append(point7_8);
              var point7_9 = $(this).find('point7text9').text();
              $('#hot24').append(point7_9);
              var point7_10 = $(this).find('point7text10').text();
              $('#hot25').append(point7_10);
              var point7_11 = $(this).find('point7text11').text();
              $('#hot26').append(point7_11);
              var point7_12 = $(this).find('point7text12').text();
              $('#hot27').append(point7_12);
              var point7_13 = $(this).find('point7text13').text();
              $('#hot28').append(point7_13);
              var point7_14 = $(this).find('point7text14').text();
              $('#hot29').append(point7_14); 
              var point7_15 = $(this).find('point7text15').text();
              $('#hot30').append(point7_15);
              var point7_15 = $(this).find('point7text16').text();
              $('#hot31').append(point7_15);
              var point7_16 = $(this).find('point7text17').text();
              $('#hot32').append(point7_16); 
            var point7_18 = $(this).find('point7text18').text();
              $('#hot33').append(point7_18); 
				
			var point5_16 = $(this).find('point7text19').text();
			$('#hot411').append(point5_16); 
			  var point5_17 = $(this).find('point7text20').text();
			$('#hot412').append(point5_17); 
			  var point5_18 = $(this).find('point7text21').text();
			$('#hot413').append(point5_18); 
			  var point5_19 = $(this).find('point7text22').text();
			$('#hot414').append(point5_19); 
			  var point5_20 = $(this).find('point7text23').text();
			$('#hot415').append(point5_20); 
			  var point5_21 = $(this).find('point7text24').text();
			$('#hot416').append(point5_21); 
			  var point5_22 = $(this).find('point7text25').text();
			$('#hot417').append(point5_22);
			
         });    
                    
          $(document).find("point8text").each(function(){
              var point8_1 = $(this).find('point8text1').text();
              $('#point8text #hot12').append(point8_1); 
               var point8_2 = $(this).find('point8text2').text();
              $('#point8text #hot13').append(point8_2);
               var point8_3 = $(this).find('point8text3').text();
              $('#point8text #hot14').append(point8_3); 
               var point8_4 = $(this).find('point8text4').text();
              $('#point8text #hot15').append(point8_4); 
               var point8_5 = $(this).find('point8text5').text();
              $('#point8text #hot16').append(point8_5); 
                var point8_6 = $(this).find('point8text6').text();
              $('.point8text11').append(point8_6);  
			   var point8_7 = $(this).find('point8text7').text();
              $('#point8text #hot114').append(point8_7); 
         });            
                    
           $(document).find("point9text").each(function(){
              var point9_1 = $(this).find('point9text1').text();
              $('#point9text li:nth-child(1)').append(point9_1); 
              
              var point9_2 = $(this).find('point9text2').text();
              $('#point9text li:nth-child(2)').append(point9_2);
              
              var point9_3 = $(this).find('point9text3').text();
              $('#point9text li:nth-child(3)').append(point9_3);
              
              var point9_4 = $(this).find('point9text4').text();
              $('#point9text li:nth-child(4)').append(point9_4); 
              
              var point9_5 = $(this).find('point9text5').text();
              $('#point9text li:nth-child(5)').append(point9_5);
              
              var point9_6 = $(this).find('point9text6').text();
              $('#point9text li:nth-child(6)').append(point9_6);
              
               var point9_7 = $(this).find('point9text7').text();
              $('#point9text li:nth-child(7)').append(point9_7);
              
              
               var point9_8 = $(this).find('point9text8').text();
              $('#hot34').append(point9_8); 
              
              var point9_9 = $(this).find('point9text9').text();
              $('#hot35').append(point9_9);
              
              var point9_10 = $(this).find('point9text10').text();
              $('#hot36').append(point9_10);
              
              var point9_11 = $(this).find('point9text11').text();
              $('#hot37').append(point9_11); 
              
              var point9_12 = $(this).find('point9text12').text();
              $('#hot38').append(point9_12);
              
              var point9_13 = $(this).find('point9text13').text();
              $('#hot39').append(point9_13);
              
               var point9_14 = $(this).find('point9text14').text();
              $('#hot40').append(point9_14);
              
               var point9_15 = $(this).find('point9text15').text();
              $('#hot41').append(point9_15); 
              
              var point9_16 = $(this).find('point9text16').text();
              $('#hot42').append(point9_16);
              
              var point9_17 = $(this).find('point9text17').text();
              $('#hot43').append(point9_17);
			   
			  var point5_16 = $(this).find('point9text18').text();
			  $('#hot311').append(point5_16); 
			  var point5_17 = $(this).find('point9text19').text();
			  $('#hot312').append(point5_17); 
			  var point5_18 = $(this).find('point9text20').text();
			  $('#hot313').append(point5_18); 
			  var point5_19 = $(this).find('point9text21').text();
			  $('#hot314').append(point5_19); 
			  var point5_20 = $(this).find('point9text22').text();
			  $('#hot315').append(point5_20); 
			  var point5_21 = $(this).find('point9text23').text();
			  $('#hot316').append(point5_21); 
			  var point5_22 = $(this).find('point9text24').text();
			  $('#hot317').append(point5_22); 
              
         });         
                    
                    
			$(document).find("point10text").each(function(){
              var point10_1 = $(this).find('point10text1').text();
              $('#point10text1').append(point10_1); 
          	});
            
            $(document).find("point12text").each(function(){
                 
             	var point12_1 = $(this).find('point12text1').text();
             	$('#point12text1').append(point12_1);
             	var point12_2 = $(this).find('point12text2').text();
             	$('#point12text2').append(point12_2);
             	var point12_3 = $(this).find('point12text3').text();
             	$('#point12text3').append(point12_3);
             	var point12_4 = $(this).find('point12text4').text();
             	$('#point12text4').append(point12_4);
             	var point12_5 = $(this).find('point12text2').text();
             	$('#point12text5').append(point12_5);
             	var point12_6 = $(this).find('point12text6').text();
             	$('#point12text6').append(point12_6);
             	var point12_7 = $(this).find('point12text7').text();
             	$('#point12text7').append(point12_7);
//             	var point12_8 = $(this).find('point12text4').text();
//             	$('#point12text8').append(point12_8);
//             	var point12_9 = $(this).find('point12text2').text();
//             	$('#point12text9').append(point12_9);
             	var point12_10 = $(this).find('point12text3').text();
             	$('#point12text10').append(point12_10);
             	var point12_11 = $(this).find('point12text11').text();
             	$('#point12text11').append(point12_11);
             	var point12_12 = $(this).find('point12text7').text();
             	$('#point12text12').append(point12_12);
//             	var point12_13 = $(this).find('point12text2').text();
//             	$('#point12text13').append(point12_13);
//             	var point12_14 = $(this).find('point12text3').text();
//             	$('#point12text14').append(point12_14);
             	var point12_15 = $(this).find('point12text4').text();
             	$('#point12text15').append(point12_15);
                 
             	var point12_li1_1 = $(this).find('point12_li1_1').text();
             	$('#point12text6 ul li:nth-child(1)').append(point12_li1_1);
             	var point12_li1_2 = $(this).find('point12_li1_2').text();
             	$('#point12text6 ul li:nth-child(2)').append(point12_li1_2);
                var point12_li1_3 = $(this).find('point12_li1_3').text();
             	$('#point12text6 ul li:nth-child(3)').append(point12_li1_3);
                 
             	var point12_li2_1 = $(this).find('point12_li2_1').text();
             	$('#point12text11 ul li:nth-child(1)').append(point12_li2_1);
             	var point12_li2_2 = $(this).find('point12_li2_2').text();
             	$('#point12text11 ul li:nth-child(2)').append(point12_li2_2);
                var point12_li2_3 = $(this).find('point12_li2_3').text();
             	$('#point12text11 ul li:nth-child(3)').append(point12_li2_3);
                 
             	var point12_li3_1 = $(this).find('point12_li3_1').text();
             	$('#point12text15 ul li:nth-child(1)').append(point12_li3_1);
             	var point12_li3_2 = $(this).find('point12_li3_2').text();
             	$('#point12text15 ul li:nth-child(2)').append(point12_li3_2);
             	var point12_li3_3 = $(this).find('point12_li3_3').text();
             	$('#point12text15 ul li:nth-child(3)').append(point12_li3_3);
                var point12_li3_4 = $(this).find('point12_li3_4').text();
             	$('#point12text15 ul li:nth-child(4)').append(point12_li3_4);
                var point12_li3_5 = $(this).find('point12_li3_5').text();
             	$('#point12text15 ul li:nth-child(5)').append(point12_li3_5);
                
                var point12_li4_1 = $(this).find('point12_li4_1').text();
             	$('#point12text12 ul li:nth-child(1)').append(point12_li4_1);
             	var point12_li4_2 = $(this).find('point12_li4_2').text();
             	$('#point12text12 ul li:nth-child(2)').append(point12_li4_2);
                 
             });       
                    
//            $(document).find("point11text").each(function(){
//                var point11_1 = $(this).find('point11text1').text();
//             	$('.point11text1').append(point11_1);  
//             });
					
           
        }, // name of the function to call upon success
                error: function(){alert("Error: Something went wrong");}
        });
}

function translateIn(no){
    $("#onloadCopy").css("opacity","1");
	//$("#point"+no+"text").fadeIn("50");
	$("#point"+no+"text > p:eq(0)").css({
	"webkitTransform":"translate(0,-5px)",
	"MozTransform":"translate(0,-5px)",
	"msTransform":"translate(0,-5px)",
	"OTransform":"translate(0,-5px)",
	"transform":"translate(0,-5px)",
        "opacity":"1"
	});
    $("#point"+no+"text > p:gt(0)").css({
	"webkitTransform":"translate(0,-5px)",
	"MozTransform":"translate(0,-5px)",
	"msTransform":"translate(0,-5px)",
	"OTransform":"translate(0,-5px)",
	"transform":"translate(0,-5px)",
        "opacity":"1"
	});
	
	$("#point"+no+"text p> ").css({
	"webkitTransform":"translate(0,-5px)",
	"MozTransform":"translate(0,-5px)",
	"msTransform":"translate(0,-5px)",
	"OTransform":"translate(0,-5px)",
	"transform":"translate(0,-5px)",
        "opacity":"1"
	});
	
	$("#point"+no+"text ul").css({
	"webkitTransform":"translate(0,-5px)",
	"MozTransform":"translate(0,-5px)",
	"msTransform":"translate(0,-5px)",
	"OTransform":"translate(0,-5px)",
	"transform":"translate(0,-5px)",
        "opacity":"1"
	});
    $("#point0image4").css({
	"webkitTransform":"translate(0,-5px)",
	"MozTransform":"translate(0,-5px)",
	"msTransform":"translate(0,-5px)",
	"OTransform":"translate(0,-5px)",
	"transform":"translate(0,-5px)",
        "opacity":"1"
	});
	$("#text1, #text2, #text3").css({
	"webkitTransform":"translate(0,-5px)",
	"MozTransform":"translate(0,-5px)",
	"msTransform":"translate(0,-5px)",
	"OTransform":"translate(0,-5px)",
	"transform":"translate(0,-5px)",
        "opacity":"0"
	});
	$(".headingText1").css('opacity','0');
	$(".headingText1").css({
		"webkitTransform":"translate(0,-5px)",
		"MozTransform":"translate(0,-5px)",
		"msTransform":"translate(0,-5px)",
		"OTransform":"translate(0,-5px)",
		"transform":"translate(0,-5px)"
	});
	$(".bodyText1").css('opacity','0');
	$(".bodyText1").css({
		"webkitTransform":"translate(0,-5px)",
		"MozTransform":"translate(0,-5px)",
		"msTransform":"translate(0,-5px)",
		"OTransform":"translate(0,-5px)",
		"transform":"translate(0,-5px)"
	});
    
//    $("#point5text1,#point5text2,#point5text3,#point5text4").css({
//		"webkitTransform":"translate(0,-5px)",
//		"MozTransform":"translate(0,-5px)",
//		"msTransform":"translate(0,-5px)",
//		"OTransform":"translate(0,-5px)",
//		"transform":"translate(0,-5px)",
//        "opcity":"1"
//	});
//	$(".heading5Text, .body5Text, .heading6Text, .body6Text, .point6text6, .point6text7, .point6text8, .point6text9, .point6text10, .point6text11, .point6text12, .heading7Text, .body7Text, .point7text6, .point7text7, .point7text8, .point7text9, .point7text10, .point7text11, .point7text12").css('opacity','0');
//	$(".heading5Text, .body5Text, .point5text6, .point5text7, .point5text8, .point5text9, .point5text10, .point5text11, .point5text12, .heading6Text, .body6Text, .point6text6, .point6text7, .point6text8, .point6text9, .point6text10, .point6text11, .point6text12, .heading7Text, .body7Text, .point7text6, .point7text7, .point7text8, .point7text9, .point7text10, .point7text11, .point7text12, .point7text1, .point7text2, .point7text3, .point7text4").css({
//		"webkitTransform":"translate(0,0px)",
//		"MozTransform":"translate(0,0px)",
//		"msTransform":"translate(0,0px)",
//		"OTransform":"translate(0,0px)",
//		"transform":"translate(0,0px)"
//	});
}

function translateOut(no){
	$("#point"+no+"text").fadeOut(500);
	$("#image"+no).css({
	"webkitTransform":"translate(0,0px)",
	"MozTransform":"translate(0,0px)",
	"msTransform":"translate(0,0px)",
	"OTransform":"translate(0,0px)",
	"transform":"translate(0,0px)",
	"opacity":0
	});
	$("#point"+no+"text > p:eq(0)").css({
	"webkitTransform":"translate(0,0px)",
	"MozTransform":"translate(0,0px)",
	"msTransform":"translate(0,0px)",
	"OTransform":"translate(0,0px)",
	"transform":"translate(0,0px)",
	"opacity":0
	});
    $("#point"+no+"text > p:gt(0)").css({
	"webkitTransform":"translate(0,0px)",
	"MozTransform":"translate(0,0px)",
	"msTransform":"translate(0,0px)",
	"OTransform":"translate(0,0px)",
	"transform":"translate(0,0px)",
	"opacity":0
	});
	$("#point"+no+"text > ul").css({
	"webkitTransform":"translate(0,0px)",
	"MozTransform":"translate(0,0px)",
	"msTransform":"translate(0,0px)",
	"OTransform":"translate(0,0px)",
	"transform":"translate(0,0px)",
	"opacity":0
	});
	$(".menu").css({
	"webkitTransform":"translate(0,0px)",
	"MozTransform":"translate(0,0px)",
	"msTransform":"translate(0,0px)",
	"OTransform":"translate(0,0px)",
	"transform":"translate(0,0px)",
	"opacity":0
	});
	$(".headingText1").css('opacity','0');
	$(".headingText1").css({
		"webkitTransform":"translate(0,0px)",
		"MozTransform":"translate(0,0px)",
		"msTransform":"translate(0,0px)",
		"OTransform":"translate(0,0px)",
		"transform":"translate(0,0px)"
	});
	$(".bodyText1").css('opacity','0');
	$(".bodyText1").css({
		"webkitTransform":"translate(0,0px)",
		"MozTransform":"translate(0,0px)",
		"msTransform":"translate(0,0px)",
		"OTransform":"translate(0,0px)",
		"transform":"translate(0,0px)"
	});	
	$("#text1, #text2, #text3").css({
	"webkitTransform":"translate(0,0px)",
	"MozTransform":"translate(0,0px)",
	"msTransform":"translate(0,0px)",
	"OTransform":"translate(0,0px)",
	"transform":"translate(0,0px)",
	"opacity":0
	});
	$(".heading5Text, .body5Text, .point5text6, .point5text7, .point5text8, .point5text9, .point5text10, .point5text11, .point5text12, .heading6Text, .body6Text, .point6text6, .point6text7, .point6text8, .point6text9, .point6text10, .point6text11, .point6text12").css('opacity','0');
	$(".heading5Text, .body5Text, .point5text6, .point5text7, .point5text8, .point5text9, .point5text10, .point5text11, .point5text12, .heading6Text, .body6Text, .point6text6, .point6text7, .point6text8, .point6text9, .point6text10, .point6text11, .point6text12").css({
		"webkitTransform":"translate(0,0px)",
		"MozTransform":"translate(0,0px)",
		"msTransform":"translate(0,0px)",
		"OTransform":"translate(0,0px)",
		"transform":"translate(0,0px)"
	});
        $("#topheading").css({
			"webkitTransform":"translate(0,0px)",
            "MozTransform":"translate(0,0px)",
            "msTransform":"translate(0,0px)",
            "OTransform":"translate(0,0px)",
            "transform":"translate(0,0px)",
			"opacity":0
	   });
         $("#onloadCopy").css({
			"webkitTransform":"translate(0,0px)",
            "MozTransform":"translate(0,0px)",
            "msTransform":"translate(0,0px)",
            "OTransform":"translate(0,0px)",
            "transform":"translate(0,0px)",
			"opacity":0
	   });
    

}