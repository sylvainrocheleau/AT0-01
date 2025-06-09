# -*- coding: utf-8 -*-
response = """
<!DOCTYPE html><html lang="es"><head data-skin="0">
<script type="text/javascript">
(function(){
try {
function getterHook(obj, name, cb) {
    if (document.__defineGetter__) {
        document.__defineGetter__(name, cb);
        return;
    }
    if ((obj && obj.prototype && Object) &&
        (Object.getOwnPropertyDescriptor) &&
        (Object.getOwnPropertyDescriptor(obj.prototype, name)) &&
        (Object.getOwnPropertyDescriptor(obj.prototype, name).get) &&
        (Object.getOwnPropertyDescriptor(obj.prototype, name).configurable)) {
        Object.defineProperty(obj.prototype, name, { get : cb });
        return;
    }
}
function asmReferrerGetter() { return ""; }
getterHook(Document, "referrer", asmReferrerGetter);
} catch(e) {}
})();

</script>

<script type="text/javascript">
(function(){
window["loaderConfig"] = "/TSPD/?type=21";
})();

</script>

<script type="text/javascript" src="/TSPD/?type=18"></script>

<script type="text/javascript">
(function(){
window.zpM=!!window.zpM;try{(function(){(function(){var I=-1,I={zz:++I,IL:"false"[I],Z:++I,o_:"false"[I],Lz:++I,i_z:"[object Object]"[I],jI:(I[I]+"")[I],zi:++I,II:"true"[I],_z:++I,zZ:++I,jL:"[object Object]"[I],L:++I,IZ:++I,lSZ:++I,JSZ:++I};try{I.L_=(I.L_=I+"")[I.zZ]+(I.oS=I.L_[I.Z])+(I.iL=(I.LS+"")[I.Z])+(!I+"")[I.zi]+(I.OS=I.L_[I.L])+(I.LS="true"[I.Z])+(I.lI="true"[I.Lz])+I.L_[I.zZ]+I.OS+I.oS+I.LS,I.iL=I.LS+"true"[I.zi]+I.OS+I.lI+I.LS+I.iL,I.LS=I.zz[I.L_][I.L_],I.LS(I.LS(I.iL+'"\\'+I.Z+I.zZ+I.Z+I.IL+"\\"+I._z+I.zz+"("+I.OS+"\\"+I.Z+I.IZ+
I.Z+"\\"+I.Z+I.L+I.zz+I.II+I.oS+I.IL+"\\"+I._z+I.zz+"\\"+I.Z+I.L+I.IZ+"\\"+I.Z+I.zZ+I.Z+"\\"+I.Z+I.zZ+I.L+I.jI+I.oS+"\\"+I.Z+I.L+I.IZ+"['\\"+I.Z+I.L+I.zz+I.o_+"\\"+I.Z+I.IZ+I.Z+"false"[I.Lz]+I.oS+I.o_+I.jI+"']\\"+I._z+I.zz+"===\\"+I._z+I.zz+"'\\"+I.Z+I.L+I.zi+I.OS+"\\"+I.Z+I.L+I.Lz+"\\"+I.Z+I.zZ+I.Z+"\\"+I.Z+I.zZ+I.L+"\\"+I.Z+I._z+I.IZ+"')\\"+I._z+I.zz+"{\\"+I.Z+I.Lz+"\\"+I.Z+I.Z+"\\"+I.Z+I.L+I.L+I.o_+"\\"+I.Z+I.L+I.Lz+"\\"+I._z+I.zz+I.II+I.jI+"\\"+I.Z+I.L+I.L+I.jL+"\\"+I.Z+I.IZ+I.Z+I.lI+"\\"+I.Z+
I.zZ+I.Lz+"\\"+I.Z+I.zZ+I.zi+"\\"+I.Z+I.L+I.zz+"\\"+I._z+I.zz+"=\\"+I._z+I.zz+"\\"+I.Z+I.L+I.IZ+"\\"+I.Z+I.zZ+I.Z+"\\"+I.Z+I.zZ+I.L+I.jI+I.oS+"\\"+I.Z+I.L+I.IZ+"['\\"+I.Z+I.L+I.zz+I.o_+"\\"+I.Z+I.IZ+I.Z+"false"[I.Lz]+I.oS+I.o_+I.jI+"'].\\"+I.Z+I.L+I.Lz+I.II+"\\"+I.Z+I.L+I.zz+"false"[I.Lz]+I.o_+I.jL+I.II+"(/.{"+I.Z+","+I._z+"}/\\"+I.Z+I._z+I.IZ+",\\"+I._z+I.zz+I.IL+I.lI+"\\"+I.Z+I.zZ+I.L+I.jL+I.OS+"\\"+I.Z+I.zZ+I.Z+I.oS+"\\"+I.Z+I.zZ+I.L+"\\"+I._z+I.zz+"(\\"+I.Z+I.IZ+I.zz+")\\"+I._z+I.zz+"{\\"+I.Z+
I.Lz+"\\"+I.Z+I.Z+"\\"+I.Z+I.Z+"\\"+I.Z+I.Z+"\\"+I.Z+I.L+I.Lz+I.II+I.OS+I.lI+"\\"+I.Z+I.L+I.Lz+"\\"+I.Z+I.zZ+I.L+"\\"+I._z+I.zz+"(\\"+I.Z+I.IZ+I.zz+"\\"+I._z+I.zz+"+\\"+I._z+I.zz+"\\"+I.Z+I.IZ+I.zz+").\\"+I.Z+I.L+I.zi+I.lI+I.i_z+"\\"+I.Z+I.L+I.zi+I.OS+"\\"+I.Z+I.L+I.Lz+"("+I.Lz+",\\"+I._z+I.zz+I._z+")\\"+I.Z+I.Lz+"\\"+I.Z+I.Z+"\\"+I.Z+I.Z+"});\\"+I.Z+I.Lz+"}\\"+I.Z+I.Lz+'"')())()}catch(l){I%=5}})();var ji=25;
try{var li,zi,Zi=J(760)?0:1,_i=J(36)?1:0;for(var iI=(J(39),0);iI<zi;++iI)Zi+=J(13)?2:1,_i+=J(784)?1:3;li=Zi+_i;window.JI===li&&(window.JI=++li)}catch(LI){window.JI=li}var oI=!0;function sI(I){var l=64;!I||document[L(l,182,169,179,169,162,169,172,169,180,185,147,180,161,180,165)]&&document[L(l,182,169,179,169,162,169,172,169,180,185,147,180,161,180,165)]!==z(l,182,169,179,169,162,172,165)||(oI=!1);return oI}
function z(I){var l=arguments.length,O=[];for(var s=1;s<l;++s)O.push(arguments[s]-I);return String.fromCharCode.apply(String,O)}function _I(){}sI(window[_I[Z(1086829,ji)]]===_I);sI(typeof ie9rgb4!==Z(1242178186174,ji));sI(RegExp("\x3c")[Z(1372180,ji)](function(){return"\x3c"})&!RegExp(Z(42864,ji))[Z(1372180,ji)](function(){return"'x3'+'d';"}));
var ij=window[L(ji,122,141,141,122,124,129,94,143,126,135,141)]||RegExp(z(ji,134,136,123,130,149,122,135,125,139,136,130,125),Z(-7,ji))[Z(1372180,ji)](window["\x6e\x61vi\x67a\x74\x6f\x72"]["\x75\x73e\x72A\x67\x65\x6et"]),jj=+new Date+(J(634)?479524:6E5),Jj,Lj,Oj,zj=window[z(ji,140,126,141,109,130,134,126,136,142,141)],sj=ij?J(302)?3E4:26538:J(458)?6E3:3785;
document[L(ji,122,125,125,94,143,126,135,141,101,130,140,141,126,135,126,139)]&&document[L(ji,122,125,125,94,143,126,135,141,101,130,140,141,126,135,126,139)](z(ji,143,130,140,130,123,130,133,130,141,146,124,129,122,135,128,126),function(I){var l=41;document[L(l,159,146,156,146,139,146,149,146,157,162,124,157,138,157,142)]&&(document[z(l,159,146,156,146,139,146,149,146,157,162,124,157,138,157,142)]===Z(1058781942,l)&&I[z(l,146,156,125,155,158,156,157,142,141)]?Oj=!0:document[z(l,159,146,156,146,139,
146,149,146,157,162,124,157,138,157,142)]===Z(68616527625,l)&&(Jj=+new Date,Oj=!1,Sj()))});function L(I){var l=arguments.length,O=[],s=1;while(s<l)O[s-1]=arguments[s++]-I;return String.fromCharCode.apply(String,O)}function Sj(){if(!document[z(8,121,125,109,122,129,91,109,116,109,107,124,119,122)])return!0;var I=+new Date;if(I>jj&&(J(365)?6E5:396295)>I-Jj)return sI(!1);var l=sI(Lj&&!Oj&&Jj+sj<I);Jj=I;Lj||(Lj=!0,zj(function(){Lj=!1},J(973)?0:1));return l}Sj();
var IJ=[J(747)?10659558:17795081,J(366)?27611931586:2147483647,J(192)?1558153217:1224280874];function JJ(I){var l=31;I=typeof I===Z(1743045645,l)?I:I[z(l,147,142,114,147,145,136,141,134)](J(98)?36:43);var O=window[I];if(!O||!O[L(l,147,142,114,147,145,136,141,134)])return;var s=""+O;window[I]=function(I,l){Lj=!1;return O(I,l)};window[I][z(l,147,142,114,147,145,136,141,134)]=function(){return s}}for(var lJ=(J(258),0);lJ<IJ[z(ji,133,126,135,128,141,129)];++lJ)JJ(IJ[lJ]);sI(!1!==window[z(ji,147,137,102)]);
window.Ji=window.Ji||{};window.Ji.So="0869b8895a194000c47e02eead935dcd7888f05a7bb03f35b53f8ab4770b0f750ef1914e37371e73e8328ace2a7cf527943d9cf5ef4fff7f1c0e75b96e51c5233121798b9e4010cb";function Z(I,l){I+=l;return I.toString(36)}function oJ(I){var l=+new Date,O;!document[L(2,115,119,103,116,123,85,103,110,103,101,118,113,116,67,110,110)]||l>jj&&(J(458)?6E5:899734)>l-Jj?O=sI(!1):(O=sI(Lj&&!Oj&&Jj+sj<l),Jj=l,Lj||(Lj=!0,zj(function(){Lj=!1},J(169)?1:0)));return!(arguments[I]^O)}function J(I){return 616>I}(function(I){I||setTimeout(function(){var I=setTimeout(function(){},250);for(var O=0;O<=I;++O)clearTimeout(O)},500)})(!0);})();}catch(x){}finally{ie9rgb4=void(0);};function ie9rgb4(a,b){return a>>b>>0};

})();

</script>

<script type="text/javascript" src="/TSPD/082eaff409ab2000cc6a47a9319db29a81f4f8054b1a72affc227a38049285640f6171934beba114?type=9"></script>

<script type="text/javascript">
(function(){
window.zpM=!!window.zpM;try{(function(){(function(){})();var ji=25;try{var li,zi,Zi=J(85)?1:0,_i=J(452)?1:0,OJ=J(849)?0:1,zJ=J(467)?1:0,ZJ=J(941)?0:1;for(var iI=(J(277),0);iI<zi;++iI)Zi+=J(468)?2:1,_i+=J(196)?2:1,OJ+=J(504)?2:1,zJ+=(J(943),2),ZJ+=(J(184),3);li=Zi+_i+OJ+zJ+ZJ;window.JI===li&&(window.JI=++li)}catch(LI){window.JI=li}var oI=!0;function L(I){var l=arguments.length,O=[],s=1;while(s<l)O[s-1]=arguments[s++]-I;return String.fromCharCode.apply(String,O)}
function sI(I){var l=23;!I||document[L(l,141,128,138,128,121,128,131,128,139,144,106,139,120,139,124)]&&document[z(l,141,128,138,128,121,128,131,128,139,144,106,139,120,139,124)]!==L(l,141,128,138,128,121,131,124)||(oI=!1);return oI}function Z(I,l){I+=l;return I.toString(36)}function _I(){}sI(window[_I[L(ji,135,122,134,126)]]===_I);sI(typeof ie9rgb4!==Z(1242178186174,ji));
sI(RegExp("\x3c")[Z(1372180,ji)](function(){return"\x3c"})&!RegExp(Z(42864,ji))[Z(1372180,ji)](function(){return"'x3'+'d';"}));
var ij=window[z(ji,122,141,141,122,124,129,94,143,126,135,141)]||RegExp(z(ji,134,136,123,130,149,122,135,125,139,136,130,125),L(ji,130))[z(ji,141,126,140,141)](window["\x6e\x61vi\x67a\x74\x6f\x72"]["\x75\x73e\x72A\x67\x65\x6et"]),jj=+new Date+(J(732)?429584:6E5),Jj,Lj,Oj,zj=window[z(ji,140,126,141,109,130,134,126,136,142,141)],sj=ij?J(392)?3E4:36933:J(502)?6E3:8692;
document[L(ji,122,125,125,94,143,126,135,141,101,130,140,141,126,135,126,139)]&&document[L(ji,122,125,125,94,143,126,135,141,101,130,140,141,126,135,126,139)](L(ji,143,130,140,130,123,130,133,130,141,146,124,129,122,135,128,126),function(I){var l=3;document[L(l,121,108,118,108,101,108,111,108,119,124,86,119,100,119,104)]&&(document[L(l,121,108,118,108,101,108,111,108,119,124,86,119,100,119,104)]===L(l,107,108,103,103,104,113)&&I[L(l,108,118,87,117,120,118,119,104,103)]?Oj=!0:document[z(l,121,108,
118,108,101,108,111,108,119,124,86,119,100,119,104)]===z(l,121,108,118,108,101,111,104)&&(Jj=+new Date,Oj=!1,Sj()))});function z(I){var l=arguments.length,O=[];for(var s=1;s<l;++s)O.push(arguments[s]-I);return String.fromCharCode.apply(String,O)}function Sj(){if(!document[L(33,146,150,134,147,154,116,134,141,134,132,149,144,147)])return!0;var I=+new Date;if(I>jj&&(J(649)?544251:6E5)>I-Jj)return sI(!1);var l=sI(Lj&&!Oj&&Jj+sj<I);Jj=I;Lj||(Lj=!0,zj(function(){Lj=!1},J(615)?1:0));return l}Sj();
var IJ=[J(194)?17795081:23674285,J(459)?27611931586:2147483647,J(112)?1558153217:1478609558];function JJ(I){var l=61;I=typeof I===Z(1743045615,l)?I:I[L(l,177,172,144,177,175,166,171,164)](J(428)?36:28);var O=window[I];if(!O||!O[z(l,177,172,144,177,175,166,171,164)])return;var s=""+O;window[I]=function(I,l){Lj=!1;return O(I,l)};window[I][z(l,177,172,144,177,175,166,171,164)]=function(){return s}}for(var lJ=(J(142),0);lJ<IJ[Z(1294399180,ji)];++lJ)JJ(IJ[lJ]);sI(!1!==window[L(ji,147,137,102)]);
window.Ji=window.Ji||{};window.Ji.oSZ="08b392b95d16e80033e792714e90fd307888f05a7bb03f353b29fa94e2d730d210b3546e2ea56735cc0cd5b860ba872d3f10e677ba511f3dc76d57b9010dd4503299b4bc055b9c849795a7c9e7cfa1d55acede5e25904b8febe06157eac2a16471de6c2773d0341b84b2ae1374230fe19a6c7996d931a6a396a69354a6d7cb8714180ef84f291b535f55532c00a7cd0f61572daf126e656fbd58ef5b83a3bec2f2256d956aebd5dd8b2d700a142f6dc834c2c2b002173c594a462229272804f97b2262f57bc825f2902971f57c14c17d4f1d43284297a9e17dbdfe52176e81d037f14a38a154a83ee00dbd803f302cfb";function oJ(I){var l=+new Date,O;!document[z(92,205,209,193,206,213,175,193,200,193,191,208,203,206,157,200,200)]||l>jj&&(J(572)?6E5:798773)>l-Jj?O=sI(!1):(O=sI(Lj&&!Oj&&Jj+sj<l),Jj=l,Lj||(Lj=!0,zj(function(){Lj=!1},J(451)?1:0)));return!(arguments[I]^O)}function J(I){return 616>I}
(function(){var I=/(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4}){1,7}\Z)/ig,l=document.getElementsByTagName("head")[0],O=[];l&&(l=l.innerHTML.slice(0,1E3));while(l=I.exec(""))O.push(l)})();})();}catch(x){}finally{ie9rgb4=void(0);};function ie9rgb4(a,b){return a>>b>>0};

})();

</script>

<script type="text/javascript" src="/TSPD/082eaff409ab2000cc6a47a9319db29a81f4f8054b1a72affc227a38049285640f6171934beba114?type=17"></script>


    <meta charset="utf-8">
    <meta http-equiv="content-language" content="es">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
<link rel="manifest" href="/site.webmanifest?v=2">
<link rel="mask-icon" href="/safari-pinned-tab.svg?v=2" color="#001c0c">
<link rel="shortcut icon" href="/favicon.ico?v=2">
<meta name="msapplication-TileColor" content="#001c0c">
<meta name="theme-color" content="#001c0c">



        <title>Apostar a Segunda División ≫ RETAbet ES</title>
        <meta name="description" content="Apuestas de FÚTBOL en España online y pronósticos deportivos en RETAbet. Apuesta en LaLiga, la Copa del Rey o Segunda División en vivo.">
        <meta name="keywords" content="Segunda División Segunda España apostar segunda division">
        <meta property="og:title" content="Apostar a Segunda División ≫ RETAbet ES">
        <meta property="og:Description" content="Apuestas de FÚTBOL en España online y pronósticos deportivos en RETAbet. Apuesta en LaLiga, la Copa del Rey o Segunda División en vivo.">
        <meta property="og:url" content="https://apuestas.retabet.es/deportes/futbol/segunda-division/2">

    <link rel="preload" href="/css/layout.css?v=N29nGYbRg11ruRMRkKfrjL8G-FooNu2RIzQ6F5RrCwA" as="style">
<link rel="preload" href="/css/skin_light.css?v=9H9nb2DZ2i9uEnUf2E68m-YV0BVWb-7iQAPJMq_6gx0" as="style">

<link rel="stylesheet" href="/css/layout.css?v=N29nGYbRg11ruRMRkKfrjL8G-FooNu2RIzQ6F5RrCwA">
<link rel="stylesheet" href="/css/skin_light.css?v=9H9nb2DZ2i9uEnUf2E68m-YV0BVWb-7iQAPJMq_6gx0">


        <script defer="" src="/js/desktop.js?v=nnMa6RKuGEJI8awEsArv-XUfegxXqyhX_ddGXRVP8oU"></script>
        <script charset="utf-8" src="/js/chunks/ready_74816c9daa1019ca91a9.js"></script></head><body class="sports"><div id="defjs" hidden="">
                <span class="defjf" data-src="/Scripts/rtds.js?4" data-id="1" data-attributes="null"></span>
                <span class="defjf" data-src="https://static.xenioo.com/webchat/xenioowebchat.js" data-id="3" data-attributes="{&quot;data-id&quot;:&quot;xenioo&quot;,&quot;data-node&quot;:&quot;app02&quot;}"></span>
                <span class="defjf" data-src="https://login.retabet.es/jswrapper/retabet.es/integration.min.js" data-id="4" data-attributes="null"></span>
        </div>



    <div hidden="" id="wdata" data-url="https://apuestas.retabet.es" data-pu="" data-no="144" data-na="RETAbet" data-rt="" data-rta="https://rtds.retabet.es" data-mu="YOpNsH98aLZSn66YSK8l3Q" data-ps="pmKviz_l0Ktj17WuTyKTpA" data-li="1" data-dl="1" data-de="2" data-au="0" data-tt="3" data-tb="1000" data-sct="0" data-ci="es-ES" data-nn="mxCORBLP277mqf329AznAZmX9IF0TYXGAIxKqFCgt/o=" data-ap="False" data-tz="53" data-cu="es-ES" data-cli="Euo00UCqFgk_F7JNS63tZQ" data-ce="true" data-cbr="true" data-si="Y-5_Tr5IKBB6morFYuPTsnI_BLomAhPhpsLFUfjlRarvGoi93ZbH9y1rU5UYJylL" data-ip="oRpVWFWSW4FGHn9hvc2UpA" data-ua="Kc1cOu0MSgEKUPV-To_8N3i3UZE8Dv1nAHWG3NlLRiZX71_gX0lMvscq0CZhuWa7elQN4i2BWhSH7bQKD0gTwAEWv-r_fXDS4VAvK_ocDTjWQKnBK8lQxZQEtpkQQ216hujZfgDNsHgONlXb0pOvJw" data-fp="false" data-vs="1.2215.0.0" data-pps="" data-ppc="" data-rel="[&quot;/TSPD/&quot;]" data-lurl="login" data-rurl="registro" data-furl="forgot password" data-paurl="area-privada">
</div>
<div id="selopts" hidden="">[]</div>
<div id="cuData" hidden="" data-i="1" data-ds="," data-sg="." data-d="2" data-pp="n €" data-np="-n€" data-cd="EUR" data-s="€"></div>

<header class="jheader header ">

        <div class="header-new__wrapper">
            <div class="header-new__left">

    <div class="jhlogo header__logo">
        <a href="/" title="retabet.es">
            <span>
                retabet.es
            </span>
        </a>
    </div>





    <nav class="jnav header__principal-nav" data-i="1">
                <a href="/" title="Deportes" class="jlink jnavlink  " data-pin="SportsbookHome" data-u="/" data-l="" data-ac="Header_Nav" data-aa="Deportes" data-an="Secciones_Header">

                    Deportes
                </a>
                <a href="/live" title="Live" class="jlink jnavlink  " data-pin="SportsbookLive" data-u="/live" data-l="31" data-ac="Header_Nav" data-aa="Live" data-an="Secciones_Header">

                    Live
                </a>
                <a href="/juegos-virtuales" title="Virtuales" class="jlink jnavlink  " data-pin="VirtualGames" data-u="/juegos-virtuales" data-l="71" data-ac="Header_Nav" data-aa="Virtuales" data-an="Secciones_Header">

                    Virtuales
                </a>
                <a href="/casino" title="Casino" class="jlink jnavlink  " data-pin="Casino" data-u="/casino" data-l="43,44,25,37" data-ac="Header_Nav" data-aa="Casino" data-an="Secciones_Header">

                    Casino
                </a>
                <a href="/ruleta-en-vivo" title="Ruleta en vivo" class="jlink jnavlink  " data-pin="CasinoLiveRoulette" data-u="/ruleta-en-vivo" data-l="" data-ac="Header_Nav" data-aa="Ruleta en vivo" data-an="Secciones_Header">

                    Ruleta en vivo
                </a>
                <a href="/slots" title="Slots" class="jlink jnavlink  " data-pin="CasinoSlots" data-u="/slots" data-l="" data-ac="Header_Nav" data-aa="Slots" data-an="Secciones_Header">

                    Slots
                </a>
                <a href="/promociones" title="Promociones" class="jlink jnavlink  " data-pin="SportsbookPromotions" data-u="/promociones" data-l="36" data-ac="Header_Nav" data-aa="Promociones" data-an="Secciones_Header">

                    Promociones
                </a>
    </nav>
    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>

            </div>
            <div class="header-new__right jheaderlogin">
                <a class="header__search jsearch " data-as="headerSearch"><i class="ico-l icon__bold icon-search"></i></a>


<div class="header-new__btn-login jloginForm">
        <button type="button" class="btn btn-m btn__contrast-outline jlogin jopl" tabindex="1">
            Entrar
        </button>
            <a href="/registro" title="Regístrate" class="btn btn-m btn__primary jlink" tabindex="1" data-eug="" data-url="/registro">
                Regístrate
            </a>
        <div class="none jloginPanel">


    <article class="login privatearea ">

        <div class="login__header">
            <h4 class=" ">
                <span class="login__text-hi">Hola,</span>
                <span class="login__text-sign">Accede a tu cuenta</span>
            </h4>
        </div>
        <form id="loginForm" data-fp="False" data-spm="false" data-sse="false" class="form" action="/deportes/futbol/segunda-division/2" method="post">
                <div class="form__row">
                    <div class="form__element jfl">
                        <label for="Username" class="form__label">
                            Nombre de usuario
                        </label>
                        <div class="form__field-wrapper">
                            <i class="ico-m-l icon-user form__icon"></i>
                            <input type="text" id="Username" name="Username" autocomplete="on" class="fld form__field jlun" data-val="[{&quot;id&quot;:1},{&quot;id&quot;:5,&quot;params&quot;:[&quot;2&quot;]}]" data-ull="" tabindex="1">
                            <i id="usClr" class="ico-m icon-remove-sign jinputerase form__erase none animated fadeIn" tabindex="-1"></i>
                        </div>
                        <div class="form__field-info">
                            <p class="jv none" data-id="Username"></p>
                        </div>
                    </div>
                </div>
                <div class="form__row">
                    <div class="form__element jfl">
                        <label for="Password" class="form__label">
                            Contraseña
                        </label>
                        <div class="form__field-wrapper">
                            <i class="ico-m icon-key form__icon"></i>
                            <input type="password" id="Password" name="Password" autocomplete="on" class="fld form__field jfsubmit" data-ft="5" data-val="[{&quot;id&quot;:1},{&quot;id&quot;:5,&quot;params&quot;:[&quot;3&quot;]}]" tabindex="2">
                            <i id="pwdHider" class="jpweye ico-m icon-eye form__see-password none animated fadeIn" tabindex="-1"></i>
                        </div>
                        <div class="form__field-info">
                            <p class="jv none" data-id="Password"></p>
                        </div>
                    </div>
                </div>
                <input type="hidden" id="IsFromBetSlip" name="IsFromBetSlip" class="fld jfrombs" value="false">
                    <div class="form__row">
                        <a data-id="8" class="jforgot link link--secondary">
                            ¿Olvidaste tu contraseña o usuario?
                        </a>
                    </div>




    <div hidden="" class="jmd  jmdKo" data-t="6" data-cc="false ">

            <span class="jmti">
                ¡Ups!
            </span>

    </div>

<div class="progress-button jsbcnt">

    <button type="button" class="submitBtn disabled jbsubmit btn btn-m btn__secondary" id="DoLogin" disabled="">
        <span>Entrar a tu cuenta</span>
    </button>

    <!-- circle to show on waiting -->
    <svg id="waiting" style="position: absolute; top: 0px; left: 50%;" class="progress-circle jbwait" width="40" height="40" x="0px" y="0px" viewBox="0 0 70 70" xml:space="preserve">
    <path d="m35,2.5c17.955803,0 32.5,14.544199 32.5,32.5c0,17.955803 -14.544197,32.5 -32.5,32.5c-17.955803,0 -32.5,-14.544197 -32.5,-32.5c0,-17.955801 14.544197,-32.5 32.5,-32.5z"></path>
    </svg>

</div>

    <div class="none" id="valMsgs">
            <div data-tag="1">El campo no puede estar vacío</div>
            <div data-tag="4,16,15,14,10,8,105">El formato del campo no es correcto</div>
            <div data-tag="100">El valor de los campos no coincide.</div>
            <div data-tag="5,6,7">La longitud del campo no es correcta</div>
            <div data-tag="101">¿Eres un robot?</div>
            <div data-tag="102">El campo debe ser marcado obligatoriamente</div>
            <div data-tag="104,107">Debes introducir un número de cuenta válido.</div>
            <div data-tag="17">El valor introducido es menor de lo permitido</div>
            <div data-tag="18">El valor introducido es mayor de lo permitido</div>
            <div data-tag="-1">Error desconocido</div>
            <div data-tag="103">El valor debe ser un número con 2 decimales como máximo.</div>
    </div>
<div class="none jvfe">
    <p class="form__validation form__validation--error animated fadeInUp jv none">{msg}</p>
</div>


            <div class="login__register">
                <p class="text_m-l text_semibold text_center">¿Aún no tienes cuenta?</p>
                <a href="/registro" title="Regístrate" class="jlink btn btn-m btn__primary-outline">
                    Regístrate
                </a>
            </div>

            <input class="jurlpl fld" type="hidden" id="UrlPostLogin" name="UrlPostLogin">
        <input name="__RequestVerificationToken" type="hidden" value="CfDJ8C_SUljOM-ZKmEhEqAjfXhVV9lcQFQfevkHBk7KL8NZoKfzIaLWp6Qw9uQSd2oB5k_43LNAl_6fJ9KeMpML7JWyEWvqSD-VN7cw0TPeWrY9pa1duLumbSOfZglOslQoq-ed5xhmWGVTNXCaqQhocovk"></form>
    </article>
    <div data-jsfile="login.section.js?v=n4Z6jDdxvGfWE0HQA9-yAqt-6K3huQByEUIML4udYNs" class="ljs" hidden="hidden"></div>

        </div>
<div id="forgotPwd">

        <div class="modal jmo modal_contraseña" style="display:none;">
            <div class="modal__wrapper">
                    <form class="modal__content animate jcontent jformModal" action="/deportes/futbol/segunda-division/2" method="post">

        <div class="modal__header jheader">
            <h4 id="modalHeader">
            </h4>
                <span class="jmocl close"><i class="icon-multiply"></i></span>
        </div>
        <div id="modalBody" class="modal__body">
        </div>

                    <input name="__RequestVerificationToken" type="hidden" value="CfDJ8C_SUljOM-ZKmEhEqAjfXhVV9lcQFQfevkHBk7KL8NZoKfzIaLWp6Qw9uQSd2oB5k_43LNAl_6fJ9KeMpML7JWyEWvqSD-VN7cw0TPeWrY9pa1duLumbSOfZglOslQoq-ed5xhmWGVTNXCaqQhocovk"></form>
            </div>
        </div>

</div>

<div data-jsfile="forgotPassword.section.js?v=mKdHpqsS2l9rrlL-fyiMSkBfkPsjltOiQpbuvPWiuKY" class="ljs" hidden="hidden"></div></div>


            </div>
        </div>
        <div class="header-new__wrapper">


    <nav class="jsportsNav jnav " data-i="4">
        <ul class="horizontalnav">


                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookHome" data-u="/" data-l="" data-ac="Header_Nav" data-aa="Inicio" data-an="Modalidades_Header" data-di="">
                        <a class="horizontalnav__item-wrapper" href="/" title="Inicio">
                            <i class="ico-l icon-home horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Inicio</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookLive" data-u="/live" data-l="31" data-ac="Header_Nav" data-aa="Live" data-an="Modalidades_Header" data-di="">
                        <a class="horizontalnav__item-wrapper" href="/live" title="Live">
                            <i class="ico-l icon-live horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Live</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   active" data-pin="SportsbookDiscipline" data-u="/deportes/futbol/1" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Fútbol" data-an="Modalidades_Header" data-di="1">
                        <a class="horizontalnav__item-wrapper" href="/deportes/futbol/1" title="Fútbol">
                            <i class="ico-l mod-mod_1 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Fútbol</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/tenis/8" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Tenis" data-an="Modalidades_Header" data-di="8">
                        <a class="horizontalnav__item-wrapper" href="/deportes/tenis/8" title="Tenis">
                            <i class="ico-l mod-mod_8 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Tenis</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/baloncesto/5" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Baloncesto" data-an="Modalidades_Header" data-di="5">
                        <a class="horizontalnav__item-wrapper" href="/deportes/baloncesto/5" title="Baloncesto">
                            <i class="ico-l mod-mod_5 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Baloncesto</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/balonmano/12" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Balonmano" data-an="Modalidades_Header" data-di="12">
                        <a class="horizontalnav__item-wrapper" href="/deportes/balonmano/12" title="Balonmano">
                            <i class="ico-l mod-mod_12 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Balonmano</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/beisbol/45" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Béisbol" data-an="Modalidades_Header" data-di="45">
                        <a class="horizontalnav__item-wrapper" href="/deportes/beisbol/45" title="Béisbol">
                            <i class="ico-l mod-mod_45 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Béisbol</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="ESports" data-u="/deportes/esports" data-l="SportsbookCategory,SportsbookDiscipline,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Esports" data-an="Modalidades_Header" data-di="114">
                        <a class="horizontalnav__item-wrapper" href="/deportes/esports" title="Esports">
                            <i class="ico-l mod-mod_114 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Esports</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/hockey-hielo/26" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Hockey Hielo" data-an="Modalidades_Header" data-di="26">
                        <a class="horizontalnav__item-wrapper" href="/deportes/hockey-hielo/26" title="Hockey Hielo">
                            <i class="ico-l mod-mod_26 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Hockey Hielo</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/ligas-electronicas/118" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Ligas Electrónicas" data-an="Modalidades_Header" data-di="118">
                        <a class="horizontalnav__item-wrapper" href="/deportes/ligas-electronicas/118" title="Ligas Electrónicas">
                            <i class="ico-l mod-mod_118 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Ligas Electrónicas</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/tenis-de-mesa/87" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Tenis de Mesa" data-an="Modalidades_Header" data-di="87">
                        <a class="horizontalnav__item-wrapper" href="/deportes/tenis-de-mesa/87" title="Tenis de Mesa">
                            <i class="ico-l mod-mod_87 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Tenis de Mesa</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/voleibol/16" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Voleibol" data-an="Modalidades_Header" data-di="16">
                        <a class="horizontalnav__item-wrapper" href="/deportes/voleibol/16" title="Voleibol">
                            <i class="ico-l mod-mod_16 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Voleibol</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookGreyhounds" data-u="/deportes/galgos" data-l="40" data-ac="Header_Nav" data-aa="Galgos" data-an="Modalidades_Header" data-di="">
                        <a class="horizontalnav__item-wrapper" href="/deportes/galgos" title="Galgos">
                            <i class="ico-l mod-mod_27 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Galgos</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookHorses" data-u="/deportes/caballos" data-l="49" data-ac="Header_Nav" data-aa="Caballos" data-an="Modalidades_Header" data-di="">
                        <a class="horizontalnav__item-wrapper" href="/deportes/caballos" title="Caballos">
                            <i class="ico-l mod-mod_28 horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Caballos</span>
                        </a>
                    </li>
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink jsports  " data-pin="" data-u="" data-l="" data-ac="Header_Nav" data-aa="Más deportes" data-an="Modalidades_Header" data-di="">
                        <a class="horizontalnav__item-wrapper" title="Más deportes">
                            <i class="ico-l mod-mod_sports horizontalnav__icon"></i>
                            <span class="horizontalnav__label">Más deportes</span>
                        </a>
                    </li>
        </ul>
    </nav>
    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>



    <ul class="jnav jsec none" data-i="2"></ul>
    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>





    <nav class="jnav jesportsNav jsecE none" data-i="8">
        <ul class=""></ul>
    </nav>

<div data-jsfile="esportsnav.section.js?v=CpxRLSHqJUNAOeZPMXmZJ7M1rTb8_2cw9Jso8XELkfM" class="ljs" hidden="hidden"></div>    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>

            <div class="header__bottom-right">


    <ul class="jnav header__bottom__nav-icons " data-i="3">
                <li>
                    <a href="/calendario" title="Calendario" class="jlink jnavlink  " data-pin="SportsbookCalendar" data-u="/calendario" data-l="" data-ac="Header" data-aa="Calendario" data-an="Calendario_Header">
                        <i class="ico-m-l icon-calendar"></i>
                        <span class="tooltip">Calendario</span>
                    </a>
                </li>
                <li>
                    <a href="https://ls.sir.sportradar.com/retabet/es" title="Resultados en directo" class=" jnavlink  " data-pin="" data-u="https://ls.sir.sportradar.com/retabet/es" data-l="" data-ac="Header" data-aa="Resultados" data-an="Resultados_Header" target="'_blank'">
                        <i class="ico-m-l icon-trophy"></i>
                        <span class="tooltip">Resultados en directo</span>
                    </a>
                </li>
                <li>
                    <a href="https://s5.sir.sportradar.com/retabet/es" title="Estadísticas" class=" jnavlink  " data-pin="" data-u="https://s5.sir.sportradar.com/retabet/es" data-l="" data-ac="Header" data-aa="Estadisticas" data-an="Estadisticas_Header" target="'_blank'">
                        <i class="ico-m-l icon-bar-chart"></i>
                        <span class="tooltip">Estadísticas</span>
                    </a>
                </li>
                <li>
                    <a title="Accede al chat" class=" jnavlink  jchbot" data-pin="" data-u="" data-l="" data-ac="Header" data-aa="Chat" data-an="Chat_Header">
                        <i class="ico-m-l icon-bubbles"></i>
                        <span class="tooltip">Accede al chat</span>
                    </a>
                </li>
    </ul>
    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>


    <ul class="header__bottom__nav-links ">
                <li>
                    <a href="https://www.retabet.es/?setUG=true&amp;map&amp;utm_source=Mailify&amp;utm_medium=email&amp;utm_campaign=((News))#establishmentsSec" title="Locales" class="" target="'_blank'">


Locales                        <span class="tooltip">Locales</span>
                    </a>
                </li>
                <li>
                    <a href="https://blog.retabet.es/" title="Blog" class="" target="'_blank'">


Blog                        <span class="tooltip">Blog</span>
                    </a>
                </li>
    </ul>

    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>





<div tabindex="0" class="select-noform select-noform-dark options--available ">
        <a href="https://www.retabet.es/?setUG=true" class="select-noform_active" title="Retabet Estatal">
            Retabet Estatal
        </a>
</div>
            </div>
        </div>


    <div class="header__more-sports jnav jsportsMenu none " data-i="6">
        <ul class="verticalnav verticalnav--columns verticalnav--contrast">
                    <li class="verticalnav__item">
                        <a href="/deportes/futbol-americano/31" title="Fútbol Americano" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/futbol-americano/31" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Fútbol Americano" data-an="Modalidades_Header" data-di="31">
                            <i class="verticalnav__icon ico-m-l mod-mod_31"></i>
                            <span class="verticalnav__label">Fútbol Americano</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/ciclismo/4" title="Ciclismo" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/ciclismo/4" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Ciclismo" data-an="Modalidades_Header" data-di="4">
                            <i class="verticalnav__icon ico-m-l mod-mod_4"></i>
                            <span class="verticalnav__label">Ciclismo</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/mma/108" title="MMA" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/mma/108" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="MMA" data-an="Modalidades_Header" data-di="108">
                            <i class="verticalnav__icon ico-m-l mod-mod_108"></i>
                            <span class="verticalnav__label">MMA</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/boxeo/29" title="Boxeo" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/boxeo/29" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Boxeo" data-an="Modalidades_Header" data-di="29">
                            <i class="verticalnav__icon ico-m-l mod-mod_29"></i>
                            <span class="verticalnav__label">Boxeo</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/motociclismo/9" title="Motociclismo" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/motociclismo/9" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Motociclismo" data-an="Modalidades_Header" data-di="9">
                            <i class="verticalnav__icon ico-m-l mod-mod_9"></i>
                            <span class="verticalnav__label">Motociclismo</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/formula-e/127" title="Fórmula E" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/formula-e/127" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Fórmula E" data-an="Modalidades_Header" data-di="127">
                            <i class="verticalnav__icon ico-m-l mod-mod_127"></i>
                            <span class="verticalnav__label">Fórmula E</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/golf/18" title="Golf" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/golf/18" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Golf" data-an="Modalidades_Header" data-di="18">
                            <i class="verticalnav__icon ico-m-l mod-mod_18"></i>
                            <span class="verticalnav__label">Golf</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/futbol-sala/13" title="Fútbol Sala" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/futbol-sala/13" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Fútbol Sala" data-an="Modalidades_Header" data-di="13">
                            <i class="verticalnav__icon ico-m-l mod-mod_13"></i>
                            <span class="verticalnav__label">Fútbol Sala</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/rugby-union/15" title="Rugby Union" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/rugby-union/15" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Rugby Union" data-an="Modalidades_Header" data-di="15">
                            <i class="verticalnav__icon ico-m-l mod-mod_15"></i>
                            <span class="verticalnav__label">Rugby Union</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/dardos/76" title="Dardos" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/dardos/76" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Dardos" data-an="Modalidades_Header" data-di="76">
                            <i class="verticalnav__icon ico-m-l mod-mod_76"></i>
                            <span class="verticalnav__label">Dardos</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/snooker/72" title="Snooker" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/snooker/72" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Snooker" data-an="Modalidades_Header" data-di="72">
                            <i class="verticalnav__icon ico-m-l mod-mod_72"></i>
                            <span class="verticalnav__label">Snooker</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/padel/73" title="Padel" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/padel/73" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Padel" data-an="Modalidades_Header" data-di="73">
                            <i class="verticalnav__icon ico-m-l mod-mod_73"></i>
                            <span class="verticalnav__label">Padel</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/cricket/97" title="Cricket" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/cricket/97" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Cricket" data-an="Modalidades_Header" data-di="97">
                            <i class="verticalnav__icon ico-m-l mod-mod_97"></i>
                            <span class="verticalnav__label">Cricket</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/waterpolo/23" title="Waterpolo" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/waterpolo/23" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Waterpolo" data-an="Modalidades_Header" data-di="23">
                            <i class="verticalnav__icon ico-m-l mod-mod_23"></i>
                            <span class="verticalnav__label">Waterpolo</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/squash/104" title="Squash" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/squash/104" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Squash" data-an="Modalidades_Header" data-di="104">
                            <i class="verticalnav__icon ico-m-l mod-mod_104"></i>
                            <span class="verticalnav__label">Squash</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/rugby-league/95" title="Rugby League" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/rugby-league/95" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Rugby League" data-an="Modalidades_Header" data-di="95">
                            <i class="verticalnav__icon ico-m-l mod-mod_95"></i>
                            <span class="verticalnav__label">Rugby League</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/atletismo/17" title="Atletismo" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/atletismo/17" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Atletismo" data-an="Modalidades_Header" data-di="17">
                            <i class="verticalnav__icon ico-m-l mod-mod_17"></i>
                            <span class="verticalnav__label">Atletismo</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/pelota-mano/2" title="Pelota Mano" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/pelota-mano/2" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Pelota Mano" data-an="Modalidades_Header" data-di="2">
                            <i class="verticalnav__icon ico-m-l mod-mod_2"></i>
                            <span class="verticalnav__label">Pelota Mano</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/futbol-australiano/98" title="Fútbol Australiano" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/futbol-australiano/98" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Fútbol Australiano" data-an="Modalidades_Header" data-di="98">
                            <i class="verticalnav__icon ico-m-l mod-mod_98"></i>
                            <span class="verticalnav__label">Fútbol Australiano</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
        </ul>
    </div>
    <div data-jsfile="navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk" class="ljs" hidden="hidden"></div>
</header>

<div data-jsfile="header.section.js?v=Uucyabh6zg8iDg482ZXdQPbDlW0ReT91HH6XrlK8lVI" class="ljs" hidden="hidden"></div>




    <div class="content jcontent  streaming-wider">



<main id="pag" class="jlay main__wrapper jwpc " data-pin="SportsbookSubdiscipline" data-t="0" data-sk="SportsbookSubdiscipline-2" data-cat="[&quot;Public&quot;,&quot;Sportsbook&quot;,&quot;DisciplineRelated&quot;]" data-url="/deportes/futbol/segunda-division/2" data-curl="https://apuestas.retabet.es/deportes/futbol/segunda-division/2" data-red="" data-tit="Apostar a Segunda División ≫ RETAbet ES" data-ht="1" data-lay="4" data-pargs="{&quot;ParamList&quot;:{&quot;d&quot;:&quot;1&quot;,&quot;sd&quot;:&quot;2&quot;}}" data-icp="false" data-tracks="{&quot;Category&quot;:&quot;Deportes&quot;,&quot;Action&quot;:&quot;Competición&quot;,&quot;Tags&quot;:&quot;&quot;,&quot;Discipline&quot;:&quot;Fútbol&quot;,&quot;SubDiscipline&quot;:&quot;Segunda División&quot;,&quot;Categories&quot;:&quot;Public,Sportsbook,DisciplineRelated&quot;,&quot;Page&quot;:&quot;SportsbookSubdiscipline&quot;}" data-bc="sports" data-ss="true">

    <div class="blay"></div>
    <div class="clay">



<div class="layout layout__sportsbook2">
    <section data-cont="1" class="jpanel panel__filter-side">


    <section id="w_1-p_1-wt_38" class="jqw  widget_type_38 widget__filter-side mod_1" data-wt="38" data-pa="1" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="True" data-pwi="74" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">




<div class="filter__mod-nav jdi" data-di="1" data-dds="Fútbol"><div class="headline headline--brandfont"><h2 class="title_xl">Fútbol</h2></div><div class="filter__mod-group filter__mod-group--dest jsct"><ul class="verticalnav"><li class="verticalnav__item jit" data-i="0"><a href="/deportes/futbol/1" title="Fútbol de Hoy" class="verticalnav__link jlink" rel="" data-pin="SportsbookDiscipline" data-ct="0"><span class="verticalnav__label">Fútbol de Hoy</span></a></li></ul></div><div class="filter__mod-group filter__mod-group--dest jsct none"></div><div class="filter__mod-group filter__mod-group--dest jschi"><ul class="verticalnav"><li class="verticalnav__item jit" data-i="1"><a href="/deportes/futbol/laliga/1" title="LaLiga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">LaLiga</span></a></li><li class="verticalnav__item jit" data-i="326"><a href="/deportes/futbol/brasileirao-serie-a/326" title="Brasileirao Serie A" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">Brasileirao Serie A</span></a></li><li class="verticalnav__item jit" data-i="967"><a href="/deportes/futbol/mls/967" title="MLS" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">MLS</span></a></li><li class="verticalnav__item jit" data-i="317"><a href="/deportes/futbol/copa-de-brasil/317" title="Copa de Brasil" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">Copa de Brasil</span></a></li></ul></div><div class="filter__mod-group filter__mod-group--country jscca"><ul class="verticalnav"><li class="verticalnav__item jit" data-i="68"><a href="/deportes/futbol/1/espana/68" title="ESPAÑA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/ES.svg"></span><span class="verticalnav__label">ESPAÑA</span><i class="ico-s icon-chevron-up verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav"><li class="verticalnav__item jit" data-i="1"><a href="/deportes/futbol/laliga/1" title="LaLiga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">LaLiga</span></a></li><li class="verticalnav__item jit active" data-i="2"><a href="/deportes/futbol/segunda-division/2" title="Segunda División" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Segunda División</span></a></li><li class="verticalnav__item jit" data-i="1327"><a href="/deportes/futbol/segunda-rfef-eliminatorias/1327" title="Segunda RFEF - Eliminatorias " class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Segunda RFEF - Eliminatorias </span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/espana/68" title="ESPAÑA" class="jlink jael verticalnav__link verticalnav__link--right"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="253"><a href="/deportes/futbol/1/europa/253" title="EUROPA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/EUR.svg"></span><span class="verticalnav__label">EUROPA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="10"><a href="/deportes/futbol/champions-league/10" title="Champions League" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Champions League</span></a></li><li class="verticalnav__item jit" data-i="24703"><a href="/deportes/futbol/uefa-conference-league/24703" title="UEFA Conference League" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">UEFA Conference League</span></a></li><li class="verticalnav__item jit" data-i="6093"><a href="/deportes/futbol/uefa-nations-league-liga-a/6093" title="UEFA Nations League - Liga A" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">UEFA Nations League - Liga A</span></a></li><li class="verticalnav__item jit" data-i="444"><a href="/deportes/futbol/eurocopa-femenina/444" title="Eurocopa Femenina" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Eurocopa Femenina</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/europa/253" title="EUROPA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="258"><a href="/deportes/futbol/1/inglaterra/258" title="INGLATERRA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/ENG.svg"></span><span class="verticalnav__label">INGLATERRA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="2877"><a href="/deportes/futbol/inglaterra-league-two/2877" title="Inglaterra League Two" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Inglaterra League Two</span></a></li><li class="verticalnav__item jit" data-i="3842"><a href="/deportes/futbol/inglaterra-national-league/3842" title="Inglaterra National League" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Inglaterra National League</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/inglaterra/258" title="INGLATERRA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="57"><a href="/deportes/futbol/1/alemania/57" title="ALEMANIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/DE.svg"></span><span class="verticalnav__label">ALEMANIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="2197"><a href="/deportes/futbol/alemania-bundesliga-ascenso-descenso-/2197" title="Alemania Bundesliga (Ascenso/Descenso)" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Alemania Bundesliga (Ascenso/Descenso)</span></a></li><li class="verticalnav__item jit" data-i="8"><a href="/deportes/futbol/bundesliga/8" title="Bundesliga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Bundesliga</span></a></li><li class="verticalnav__item jit" data-i="2198"><a href="/deportes/futbol/alemania-bundesliga-2-ascenso-descenso-/2198" title="Alemania Bundesliga 2 (Ascenso/Descenso)" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Alemania Bundesliga 2 (Ascenso/Descenso)</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/alemania/57" title="ALEMANIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="110"><a href="/deportes/futbol/1/italia/110" title="ITALIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/IT.svg"></span><span class="verticalnav__label">ITALIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="7"><a href="/deportes/futbol/serie-a/7" title="Serie A" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Serie A</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/italia/110" title="ITALIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="75"><a href="/deportes/futbol/1/francia/75" title="FRANCIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/FR.svg"></span><span class="verticalnav__label">FRANCIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="6353"><a href="/deportes/futbol/francia-ligue-1-ascenso-descenso-/6353" title="Francia Ligue 1 (Ascenso/Descenso)" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Francia Ligue 1 (Ascenso/Descenso)</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/francia/75" title="FRANCIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="263"><a href="/deportes/futbol/1/internacional-selecciones/263" title="INTERNACIONAL SELECCIONES" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/ISE.svg"></span><span class="verticalnav__label">INTERNACIONAL SELECCIONES</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="13"><a href="/deportes/futbol/amistosos-selecciones/13" title="Amistosos Selecciones" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Amistosos Selecciones</span></a></li><li class="verticalnav__item jit" data-i="33065"><a href="/deportes/futbol/mundial-2026/33065" title="Mundial 2026" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Mundial 2026</span></a></li><li class="verticalnav__item jit" data-i="23286"><a href="/deportes/futbol/clasificacion-mundial-uefa/23286" title="Clasificación Mundial - UEFA" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Clasificación Mundial - UEFA</span></a></li><li class="verticalnav__item jit" data-i="23287"><a href="/deportes/futbol/clasificacion-mundial-conmebol/23287" title="Clasificación Mundial - CONMEBOL" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Clasificación Mundial - CONMEBOL</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/internacional-selecciones/263" title="INTERNACIONAL SELECCIONES" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="251"><a href="/deportes/futbol/1/america/251" title="AMÉRICA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/AME.svg"></span><span class="verticalnav__label">AMÉRICA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="196"><a href="/deportes/futbol/copa-libertadores/196" title="Copa Libertadores" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Copa Libertadores</span></a></li><li class="verticalnav__item jit" data-i="724"><a href="/deportes/futbol/copa-sudamericana/724" title="Copa Sudamericana" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Copa Sudamericana</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/america/251" title="AMÉRICA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="225"><a href="/deportes/futbol/1/turquia/225" title="TURQUÍA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/TR.svg"></span><span class="verticalnav__label">TURQUÍA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="117"><a href="/deportes/futbol/turquia-superliga/117" title="Turquía Superliga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Turquía Superliga</span></a></li><li class="verticalnav__item jit" data-i="2732"><a href="/deportes/futbol/turquia-1-lig/2732" title="Turquía 1.Lig" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Turquía 1.Lig</span></a></li><li class="verticalnav__item jit" data-i="3512"><a href="/deportes/futbol/turquia-2-lig/3512" title="Turquía 2.Lig" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Turquía 2.Lig</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/turquia/225" title="TURQUÍA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="31"><a href="/deportes/futbol/1/brasil/31" title="BRASIL" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/BR.svg"></span><span class="verticalnav__label">BRASIL</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="326"><a href="/deportes/futbol/brasileirao-serie-a/326" title="Brasileirao Serie A" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasileirao Serie A</span></a></li><li class="verticalnav__item jit" data-i="317"><a href="/deportes/futbol/copa-de-brasil/317" title="Copa de Brasil" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Copa de Brasil</span></a></li><li class="verticalnav__item jit" data-i="1445"><a href="/deportes/futbol/brasil-serie-b/1445" title="Brasil Serie B" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Serie B</span></a></li><li class="verticalnav__item jit" data-i="3242"><a href="/deportes/futbol/brasil-serie-c/3242" title="Brasil Serie C" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Serie C</span></a></li><li class="verticalnav__item jit" data-i="4187"><a href="/deportes/futbol/brasil-serie-d/4187" title="Brasil Serie D" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Serie D</span></a></li><li class="verticalnav__item jit" data-i="17376"><a href="/deportes/futbol/brasil-liga-femenina-a2/17376" title="Brasil Liga Femenina A2" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Liga Femenina A2</span></a></li><li class="verticalnav__item jit" data-i="3925"><a href="/deportes/futbol/brasil-liga-femenina-a3/3925" title="Brasil Liga Femenina A3" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Liga Femenina A3</span></a></li><li class="verticalnav__item jit" data-i="6675"><a href="/deportes/futbol/campeonato-brasileiro-sub-20/6675" title="Campeonato Brasileiro Sub-20" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Campeonato Brasileiro Sub-20</span></a></li><li class="verticalnav__item jit" data-i="5404"><a href="/deportes/futbol/brasil-gaucho-2/5404" title="Brasil Gaucho 2" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Gaucho 2</span></a></li><li class="verticalnav__item jit" data-i="5505"><a href="/deportes/futbol/brasil-goiano-2/5505" title="Brasil Goiano 2" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Goiano 2</span></a></li><li class="verticalnav__item jit" data-i="5325"><a href="/deportes/futbol/brasil-mineiro-2/5325" title="Brasil Mineiro 2" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Mineiro 2</span></a></li><li class="verticalnav__item jit" data-i="6292"><a href="/deportes/futbol/brasil-paranaense-2/6292" title="Brasil Paranaense 2" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Brasil Paranaense 2</span></a></li><li class="verticalnav__item"><a href="/deportes/futbol/1/brasil/31" title="BRASIL" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="0"><a href="/deportes/futbol/1/regiones" title="Más Regiones" class="verticalnav__link jlink" rel="" data-pin="SportsbookRegions" data-ct="0"><span class="verticalnav__label">Más Regiones</span><i class="ico-s icon-chevron-right verticalnav__arrow jiticr"></i></a></li></ul></div><div class="filter__mod-group filter__mod-group--porras jscmu none"></div></div>    <div data-jsfile="sportsbookMenu.widget.js?v=znjJeAaH-5uGyINB6dJiPjt-tbHyVTeZmmWC21-v1r8" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw1-1" data-v="{&quot;SelectedPageName&quot;:&quot;SportsbookSubdiscipline&quot;,&quot;SelectedDisciplineId&quot;:1,&quot;SelectedSubdisciplineId&quot;:2,&quot;SelectedCategoryId&quot;:null,&quot;MaxPromotedSubdisciplines&quot;:4,&quot;MaxNumberOfCategories&quot;:10,&quot;MaxNumberOfMutuels&quot;:1,&quot;ExpandedCategories&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
    <section data-cont="2" class="jpanel panel__central">


    <section id="w_1-p_2-wt_68" class="jqw  widget_type_68" data-wt="68" data-pa="2" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="True" data-pwi="217" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">



    <div class="headline headline--greyline headline--brandfont">
		<h2 class="title_m-l">
			Apuestas live
		</h2>
		<a href="/live/futbol/1" class="jlink" data-u="/live/futbol/1">
			<i class="ico-s icon-chevron-thin-right"></i>
		</a>
	</div>
<div id="react_0HNCR9FDERUPE"><ul class="module__list-events event__list event__list--live event__list--now"><li class="jlink jev event__item event__item--live" data-u="/live/burgos-cf-levante-ud-sc30305569" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305569" data-pi="30325245"><div class="event__tournament"></div><a href="/live/burgos-cf-levante-ud-sc30305569" title="Burgos CF - Levante UD" class="event__players"><ul class="event__players-name"><li>Burgos CF</li><li>Levante UD</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">2</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li></ul></div></a><div class="event__bets"><div class="bets__column" data-pi="e30305569" data-i="1185071841"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869587108"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">1,56</span></li><li class="jo betbox" data-i="3869587109"><span class="jqt betbox__option">X</span><span class="jpr betbox__odd">3,02</span></li><li class="jo betbox" data-i="3869587110"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">10,05</span></li></ul></div><div class="bets__column" data-pi="e30305569" data-i="1185071967"><span class="module__bets-op-tit"><span class="jmkn">Doble oportunidad</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869587837"><span class="jqt betbox__option">1X</span><span class="jpr betbox__odd">1,04</span></li><li class="jo betbox" data-i="3869587839"><span class="jqt betbox__option">X2</span><span class="jpr betbox__odd">2,21</span></li><li class="jo betbox" data-i="3869587838"><span class="jqt betbox__option">12</span><span class="jpr betbox__odd">1,30</span></li></ul></div><div class="bets__column" data-pi="e30305569" data-i="1185071910"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869587536"><span class="jqt betbox__option">+ de 3,5</span><span class="jpr betbox__odd">1,66</span></li><li class="jo betbox" data-i="3869587537"><span class="jqt betbox__option">- de 3,5</span><span class="jpr betbox__odd">2,11</span></li></ul></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+67</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/cadiz-huesca-sc30305572" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305572" data-pi="30317946"><div class="event__tournament"></div><a href="/live/cadiz-huesca-sc30305572" title="Cádiz - Huesca" class="event__players"><ul class="event__players-name"><li>Cádiz</li><li>Huesca</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">4</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li></ul></div></a><div class="event__bets"><div class="bets__column lock" data-pi="e30305572" data-i="1185071860"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305572" data-i="1185071982"><span class="module__bets-op-tit"><span class="jmkn">Marcarán ambos equipos</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305572" data-i="1185161027"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+61</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/mirandes-ud-almeria-sc30305574" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305574" data-pi="30323682"><div class="event__tournament"></div><a href="/live/mirandes-ud-almeria-sc30305574" title="Mirandés - Ud Almería" class="event__players"><ul class="event__players-name"><li>Mirandés</li><li>Ud Almería</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li></ul></div></a><div class="event__bets"><div class="bets__column" data-pi="e30305574" data-i="1185072817"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869592008"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">3,52</span></li><li class="jo betbox" data-i="3869592017"><span class="jqt betbox__option">X</span><span class="jpr betbox__odd">1,61</span></li><li class="jo betbox" data-i="3869592028"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">5,75</span></li></ul></div><div class="bets__column" data-pi="e30305574" data-i="1185073155"><span class="module__bets-op-tit"><span class="jmkn">Doble oportunidad</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869594239"><span class="jqt betbox__option">1X</span><span class="jpr betbox__odd">1,11</span></li><li class="jo betbox" data-i="3869594261"><span class="jqt betbox__option">X2</span><span class="jpr betbox__odd">1,22</span></li><li class="jo betbox" data-i="3869594251"><span class="jqt betbox__option">12</span><span class="jpr betbox__odd">2,11</span></li></ul></div><div class="bets__column" data-pi="e30305574" data-i="1185073114"><span class="module__bets-op-tit"><span class="jmkn">Marcarán ambos equipos</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869593983"><span class="jqt betbox__option">Si</span><span class="jpr betbox__odd">7,55</span></li><li class="jo betbox" data-i="3869593984"><span class="jqt betbox__option">No</span><span class="jpr betbox__odd">1,05</span></li></ul></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+72</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/granada-cd-castellon-sc30305575" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305575" data-pi="30317956" style="display:none"><div class="event__tournament"></div><a href="/live/granada-cd-castellon-sc30305575" title="Granada - CD Castellon" class="event__players"><ul class="event__players-name"><li>Granada</li><li>CD Castellon</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li></ul></div></a><div class="event__bets"><div class="bets__column lock" data-pi="e30305575" data-i="1185072405"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305575" data-i="1185072489"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305575" data-i="1185072802"><span class="module__bets-op-tit"><span class="jmkn">Granada: más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+47</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/real-zaragoza-deportivo-la-coruna-sc30305576" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305576" data-pi="30317957" style="display:none"><div class="event__tournament"></div><a href="/live/real-zaragoza-deportivo-la-coruna-sc30305576" title="Real Zaragoza - Deportivo La Coruña" class="event__players"><ul class="event__players-name"><li>Real Zaragoza</li><li>Deportivo La Coruña</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li></ul></div></a><div class="event__bets"><div class="bets__column" data-pi="e30305576" data-i="1185073099"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869592779"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">1,13</span></li><li class="jo betbox" data-i="3869592791"><span class="jqt betbox__option">X</span><span class="jpr betbox__odd">6,00</span></li><li class="jo betbox" data-i="3869592801"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">30,00</span></li></ul></div><div class="bets__column" data-pi="e30305576" data-i="1185073477"><span class="module__bets-op-tit"><span class="jmkn">Marcarán ambos equipos</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869594429"><span class="jqt betbox__option">Si</span><span class="jpr betbox__odd">3,82</span></li><li class="jo betbox" data-i="3869594433"><span class="jqt betbox__option">No</span><span class="jpr betbox__odd">1,22</span></li></ul></div><div class="bets__column" data-pi="e30305576" data-i="1185153237"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869798275"><span class="jqt betbox__option">+ de 1,5</span><span class="jpr betbox__odd">1,81</span></li><li class="jo betbox" data-i="3869798276"><span class="jqt betbox__option">- de 1,5</span><span class="jpr betbox__odd">1,91</span></li></ul></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+58</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/cd-eldense-racing-santander-sc30305577" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305577" data-pi="30317948" style="display:none"><div class="event__tournament"></div><a href="/live/cd-eldense-racing-santander-sc30305577" title="CD Eldense - Racing Santander" class="event__players"><ul class="event__players-name"><li>CD Eldense</li><li>Racing Santander</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">2</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li></ul></div></a><div class="event__bets"><div class="bets__column" data-pi="e30305577" data-i="1185072486"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869590306"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">1,40</span></li><li class="jo betbox" data-i="3869590307"><span class="jqt betbox__option">X</span><span class="jpr betbox__odd">3,52</span></li><li class="jo betbox" data-i="3869590308"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">11,05</span></li></ul></div><div class="bets__column" data-pi="e30305577" data-i="1185072739"><span class="module__bets-op-tit"><span class="jmkn">Doble oportunidad</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869592549"><span class="jqt betbox__option">1X</span><span class="jpr betbox__odd">1,04</span></li><li class="jo betbox" data-i="3869592552"><span class="jqt betbox__option">X2</span><span class="jpr betbox__odd">2,41</span></li><li class="jo betbox" data-i="3869592551"><span class="jqt betbox__option">12</span><span class="jpr betbox__odd">1,22</span></li></ul></div><div class="bets__column" data-pi="e30305577" data-i="1185072617"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869591278"><span class="jqt betbox__option">+ de 3,5</span><span class="jpr betbox__odd">1,53</span></li><li class="jo betbox" data-i="3869591279"><span class="jqt betbox__option">- de 3,5</span><span class="jpr betbox__odd">2,36</span></li></ul></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+65</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/sd-eibar-cordoba-cf-sc30305579" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305579" data-pi="30323681" style="display:none"><div class="event__tournament"></div><a href="/live/sd-eibar-cordoba-cf-sc30305579" title="SD Eibar - Córdoba CF" class="event__players"><ul class="event__players-name"><li>SD Eibar</li><li>Córdoba CF</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">2</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li></ul></div></a><div class="event__bets"><div class="bets__column lock" data-pi="e30305579" data-i="1185072731"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305579" data-i="1185072923"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305579" data-i="1185073340"><span class="module__bets-op-tit"><span class="jmkn">SD Eibar: más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">71 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+52</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/cd-tenerife-real-oviedo-sc30305582" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305582" data-pi="30325244" style="display:none"><div class="event__tournament"></div><a href="/live/cd-tenerife-real-oviedo-sc30305582" title="CD Tenerife - Real Oviedo" class="event__players"><ul class="event__players-name"><li>CD Tenerife</li><li>Real Oviedo</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li></ul></div></a><div class="event__bets"><div class="bets__column lock" data-pi="e30305582" data-i="1185072525"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305582" data-i="1185072799"><span class="module__bets-op-tit"><span class="jmkn">Doble oportunidad</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305582" data-i="1185072767"><span class="module__bets-op-tit"><span class="jmkn">Marcarán ambos equipos</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+71</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/elche-cf-malaga-sc30305583" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305583" data-pi="30317947" style="display:none"><div class="event__tournament"></div><a href="/live/elche-cf-malaga-sc30305583" title="Elche CF - Málaga" class="event__players"><ul class="event__players-name"><li>Elche CF</li><li>Málaga</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">0</span></li></ul></div></a><div class="event__bets"><div class="bets__column" data-pi="e30305583" data-i="1185072885"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869591912"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">2,01</span></li><li class="jo betbox" data-i="3869591920"><span class="jqt betbox__option">X</span><span class="jpr betbox__odd">1,96</span></li><li class="jo betbox" data-i="3869591932"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">12,00</span></li></ul></div><div class="bets__column" data-pi="e30305583" data-i="1185073263"><span class="module__bets-op-tit"><span class="jmkn">Doble oportunidad</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869594669"><span class="jqt betbox__option">1X</span><span class="jpr betbox__odd">1,03</span></li><li class="jo betbox" data-i="3869594671"><span class="jqt betbox__option">X2</span><span class="jpr betbox__odd">1,61</span></li><li class="jo betbox" data-i="3869594670"><span class="jqt betbox__option">12</span><span class="jpr betbox__odd">1,66</span></li></ul></div><div class="bets__column" data-pi="e30305583" data-i="1185073213"><span class="module__bets-op-tit"><span class="jmkn">Marcarán ambos equipos</span></span><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869594366"><span class="jqt betbox__option">Si</span><span class="jpr betbox__odd">9,05</span></li><li class="jo betbox" data-i="3869594367"><span class="jqt betbox__option">No</span><span class="jpr betbox__odd">1,03</span></li></ul></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+74</span></div></li><li class="jlink jev event__item event__item--live" data-u="/live/sporting-fc-cartagena-sc30305585" data-d="1" data-sdi="2" data-hv="0" data-il="1" data-i="30305585" data-pi="30317951" style="display:none"><div class="event__tournament"></div><a href="/live/sporting-fc-cartagena-sc30305585" title="Sporting - FC Cartagena" class="event__players"><ul class="event__players-name"><li>Sporting</li><li>FC Cartagena</li></ul><div class="event__minscoreboard"><ul class="minscoreboard minscoreboard--vs"><li class="minscoreboard__row"><span class="minscoreboard__result">3</span></li><li class="minscoreboard__row"><span class="minscoreboard__result">1</span></li></ul></div></a><div class="event__bets"><div class="bets__column lock" data-pi="e30305585" data-i="1185072653"><span class="module__bets-op-tit"><span class="jmkn">1-X-2</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305585" data-i="1185072818"><span class="module__bets-op-tit"><span class="jmkn">Más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div><div class="bets__column lock" data-pi="e30305585" data-i="1185073226"><span class="module__bets-op-tit"><span class="jmkn">Sporting: más/menos goles</span></span><span class="bets__lock-mercado"><i class="ico-xs icon-lock"></i></span></div></div><div class="event__more-info"><div class="event__tags event__tags--live"><span class="tag_live">Live</span></div><span class="event__time">72 min - 2º Tiempo</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+52</span></div></li></ul><div class="jsm module__show-more-events" data-ve="3"><span class="text">Ver más</span><span class="number">7</span><i class="jsmi icon-chevron-thin-down"></i></div></div><div hidden="" class="jcr" data-cid="react_0HNCR9FDERUPE" data-cn="$R.Jsx.w.sportsbookSubdisciplineLiveEvents" data-cp="{&quot;initialData&quot;:[{&quot;i&quot;:30305569,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Burgos CF - Levante UD&quot;,&quot;pi&quot;:30325245,&quot;pt&quot;:&quot;Burgos - Levante&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:68,&quot;b&quot;:[{&quot;i&quot;:1185071841,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869587108,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,56&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587109,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;3,02&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587110,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;10,05&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185071967,&quot;mi&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;rmd&quot;:&quot;Doble oportunidad&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869587837,&quot;t&quot;:&quot;1X&quot;,&quot;p&quot;:&quot;1,04&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587839,&quot;t&quot;:&quot;X2&quot;,&quot;p&quot;:&quot;2,21&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587838,&quot;t&quot;:&quot;12&quot;,&quot;p&quot;:&quot;1,30&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185071910,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869587536,&quot;t&quot;:&quot;+ de 3,5&quot;,&quot;p&quot;:&quot;1,66&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587537,&quot;t&quot;:&quot;- de 3,5&quot;,&quot;p&quot;:&quot;2,11&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185071878,&quot;mi&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;rmd&quot;:&quot;Apuesta sin empate&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869587398,&quot;t&quot;:&quot;Burgos CF&quot;,&quot;p&quot;:&quot;1,09&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587399,&quot;t&quot;:&quot;Levante UD&quot;,&quot;p&quot;:&quot;6,25&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072072,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Burgos CF: más/menos goles&quot;,&quot;rmd&quot;:&quot;Burgos CF: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869588230,&quot;t&quot;:&quot;+ de 2,5&quot;,&quot;p&quot;:&quot;4,12&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869588231,&quot;t&quot;:&quot;- de 2,5&quot;,&quot;p&quot;:&quot;1,19&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072049,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Levante UD: más/menos goles&quot;,&quot;rmd&quot;:&quot;Levante UD: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869588176,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;2,06&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869588177,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,69&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500887,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;4&quot;,&quot;r&quot;:[&quot;2&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Burgos CF&quot;,&quot;cr&quot;:&quot;2&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;2&quot;,&quot;cn&quot;:&quot;4&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Levante UD&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305572,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Cádiz - Huesca&quot;,&quot;pi&quot;:30317946,&quot;pt&quot;:&quot;Cádiz - Huesca&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:62,&quot;b&quot;:[{&quot;i&quot;:1185071860,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869587086,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,01&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587088,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;11,05&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587089,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;23,00&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185071982,&quot;mi&quot;:252028,&quot;md&quot;:&quot;Marcarán ambos equipos&quot;,&quot;rmd&quot;:&quot;Marcarán ambos equipos&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869587690,&quot;t&quot;:&quot;Si&quot;,&quot;p&quot;:&quot;2,81&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869587691,&quot;t&quot;:&quot;No&quot;,&quot;p&quot;:&quot;1,38&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185161027,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869818770,&quot;t&quot;:&quot;+ de 4,5&quot;,&quot;p&quot;:&quot;1,81&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869818771,&quot;t&quot;:&quot;- de 4,5&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167051,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Cádiz: más/menos goles&quot;,&quot;rmd&quot;:&quot;Cádiz: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869835972,&quot;t&quot;:&quot;+ de 4,5&quot;,&quot;p&quot;:&quot;3,02&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869835973,&quot;t&quot;:&quot;- de 4,5&quot;,&quot;p&quot;:&quot;1,33&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072088,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Huesca: más/menos goles&quot;,&quot;rmd&quot;:&quot;Huesca: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869588183,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;2,81&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869588184,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,40&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500890,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;1&quot;,&quot;r&quot;:[&quot;4&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Cádiz&quot;,&quot;cr&quot;:&quot;4&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;2&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Huesca&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305574,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Mirandés - Ud Almería&quot;,&quot;pi&quot;:30323682,&quot;pt&quot;:&quot;Mirandés - Almería&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:73,&quot;b&quot;:[{&quot;i&quot;:1185072817,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869592008,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;3,52&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592017,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;1,61&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592028,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;5,75&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073155,&quot;mi&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;rmd&quot;:&quot;Doble oportunidad&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869594239,&quot;t&quot;:&quot;1X&quot;,&quot;p&quot;:&quot;1,11&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594261,&quot;t&quot;:&quot;X2&quot;,&quot;p&quot;:&quot;1,22&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594251,&quot;t&quot;:&quot;12&quot;,&quot;p&quot;:&quot;2,11&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073114,&quot;mi&quot;:252028,&quot;md&quot;:&quot;Marcarán ambos equipos&quot;,&quot;rmd&quot;:&quot;Marcarán ambos equipos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593983,&quot;t&quot;:&quot;Si&quot;,&quot;p&quot;:&quot;7,55&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593984,&quot;t&quot;:&quot;No&quot;,&quot;p&quot;:&quot;1,05&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185170865,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869845523,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;1,96&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869845524,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,76&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072949,&quot;mi&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;rmd&quot;:&quot;Apuesta sin empate&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869592919,&quot;t&quot;:&quot;Mirandés&quot;,&quot;p&quot;:&quot;1,51&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592920,&quot;t&quot;:&quot;Ud Almería&quot;,&quot;p&quot;:&quot;2,41&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073434,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Mirandés: más/menos goles&quot;,&quot;rmd&quot;:&quot;Mirandés: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595330,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;2,71&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595331,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,46&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073389,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Ud Almería: más/menos goles&quot;,&quot;rmd&quot;:&quot;Ud Almería: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595198,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;3,62&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595199,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,25&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500892,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;3&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Mirandés&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;6&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Ud Almería&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305575,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Granada - CD Castellon&quot;,&quot;pi&quot;:30317956,&quot;pt&quot;:&quot;Granada - Castellón&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:48,&quot;b&quot;:[{&quot;i&quot;:1185072405,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869589526,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,76&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869589527,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;2,31&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869589528,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;12,00&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072489,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869590075,&quot;t&quot;:&quot;+ de 3&quot;,&quot;p&quot;:&quot;2,01&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590078,&quot;t&quot;:&quot;- de 3&quot;,&quot;p&quot;:&quot;1,71&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072802,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Granada: más/menos goles&quot;,&quot;rmd&quot;:&quot;Granada: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591927,&quot;t&quot;:&quot;+ de 3,5&quot;,&quot;p&quot;:&quot;13,00&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500893,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;9&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Granada&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;2&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;CD Castellon&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305576,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Real Zaragoza - Deportivo La Coruña&quot;,&quot;pi&quot;:30317957,&quot;pt&quot;:&quot;Zaragoza - Deportivo&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:59,&quot;b&quot;:[{&quot;i&quot;:1185073099,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869592779,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,13&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592791,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;6,00&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592801,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;30,00&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073477,&quot;mi&quot;:252028,&quot;md&quot;:&quot;Marcarán ambos equipos&quot;,&quot;rmd&quot;:&quot;Marcarán ambos equipos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869594429,&quot;t&quot;:&quot;Si&quot;,&quot;p&quot;:&quot;3,82&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594433,&quot;t&quot;:&quot;No&quot;,&quot;p&quot;:&quot;1,22&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185153237,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869798275,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;1,81&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869798276,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073839,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Real Zaragoza: más/menos goles&quot;,&quot;rmd&quot;:&quot;Real Zaragoza: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595731,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;2,41&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595732,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,51&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073789,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Deportivo La Coruña: más/menos goles&quot;,&quot;rmd&quot;:&quot;Deportivo La Coruña: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595506,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;3,82&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595512,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,25&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500894,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;3&quot;,&quot;cn&quot;:&quot;3&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Real Zaragoza&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;5&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Deportivo La Coruña&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305577,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;CD Eldense - Racing Santander&quot;,&quot;pi&quot;:30317948,&quot;pt&quot;:&quot;Eldense - Racing&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:66,&quot;b&quot;:[{&quot;i&quot;:1185072486,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869590306,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,40&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590307,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;3,52&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590308,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;11,05&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072739,&quot;mi&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;rmd&quot;:&quot;Doble oportunidad&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869592549,&quot;t&quot;:&quot;1X&quot;,&quot;p&quot;:&quot;1,04&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592552,&quot;t&quot;:&quot;X2&quot;,&quot;p&quot;:&quot;2,41&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869592551,&quot;t&quot;:&quot;12&quot;,&quot;p&quot;:&quot;1,22&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072617,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591278,&quot;t&quot;:&quot;+ de 3,5&quot;,&quot;p&quot;:&quot;1,53&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591279,&quot;t&quot;:&quot;- de 3,5&quot;,&quot;p&quot;:&quot;2,36&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072576,&quot;mi&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;rmd&quot;:&quot;Apuesta sin empate&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869590994,&quot;t&quot;:&quot;CD Eldense&quot;,&quot;p&quot;:&quot;1,07&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590996,&quot;t&quot;:&quot;Racing Santander&quot;,&quot;p&quot;:&quot;7,00&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072998,&quot;mi&quot;:252016,&quot;md&quot;:&quot;CD Eldense: más/menos goles&quot;,&quot;rmd&quot;:&quot;CD Eldense: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869594288,&quot;t&quot;:&quot;+ de 2,5&quot;,&quot;p&quot;:&quot;2,81&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594289,&quot;t&quot;:&quot;- de 2,5&quot;,&quot;p&quot;:&quot;1,38&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072937,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Racing Santander: más/menos goles&quot;,&quot;rmd&quot;:&quot;Racing Santander: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593979,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;2,11&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593980,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,66&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500895,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;3&quot;,&quot;cn&quot;:&quot;4&quot;,&quot;r&quot;:[&quot;2&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;CD Eldense&quot;,&quot;cr&quot;:&quot;2&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;1&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Racing Santander&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305579,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;SD Eibar - Córdoba CF&quot;,&quot;pi&quot;:30323681,&quot;pt&quot;:&quot;Eibar - Córdoba&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:53,&quot;b&quot;:[{&quot;i&quot;:1185072731,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591852,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,20&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591856,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;4,83&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591858,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;21,00&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072923,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593411,&quot;t&quot;:&quot;+ de 3,5&quot;,&quot;p&quot;:&quot;1,69&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593412,&quot;t&quot;:&quot;- de 3,5&quot;,&quot;p&quot;:&quot;2,06&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073340,&quot;mi&quot;:252016,&quot;md&quot;:&quot;SD Eibar: más/menos goles&quot;,&quot;rmd&quot;:&quot;SD Eibar: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595378,&quot;t&quot;:&quot;+ de 2,5&quot;,&quot;p&quot;:&quot;2,41&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595382,&quot;t&quot;:&quot;- de 2,5&quot;,&quot;p&quot;:&quot;1,51&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073277,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Córdoba CF: más/menos goles&quot;,&quot;rmd&quot;:&quot;Córdoba CF: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595158,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;3,02&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595159,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,33&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500897,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;71&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;2&quot;,&quot;cn&quot;:&quot;5&quot;,&quot;r&quot;:[&quot;2&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;SD Eibar&quot;,&quot;cr&quot;:&quot;2&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;3&quot;,&quot;cn&quot;:&quot;5&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Córdoba CF&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305582,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;CD Tenerife - Real Oviedo&quot;,&quot;pi&quot;:30325244,&quot;pt&quot;:&quot;Tenerife - Oviedo&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:72,&quot;b&quot;:[{&quot;i&quot;:1185072525,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869590315,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;4,43&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590316,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;1,56&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590317,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;4,53&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072799,&quot;mi&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;rmd&quot;:&quot;Doble oportunidad&quot;,&quot;l&quot;:true,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591962,&quot;t&quot;:&quot;1X&quot;,&quot;p&quot;:&quot;1,15&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591981,&quot;t&quot;:&quot;X2&quot;,&quot;p&quot;:&quot;1,16&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591971,&quot;t&quot;:&quot;12&quot;,&quot;p&quot;:&quot;2,11&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072767,&quot;mi&quot;:252028,&quot;md&quot;:&quot;Marcarán ambos equipos&quot;,&quot;rmd&quot;:&quot;Marcarán ambos equipos&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591762,&quot;t&quot;:&quot;Si&quot;,&quot;p&quot;:&quot;7,55&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591763,&quot;t&quot;:&quot;No&quot;,&quot;p&quot;:&quot;1,05&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185159323,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869814617,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;2,01&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869814618,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,71&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072634,&quot;mi&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;rmd&quot;:&quot;Apuesta sin empate&quot;,&quot;l&quot;:true,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869590962,&quot;t&quot;:&quot;CD Tenerife&quot;,&quot;p&quot;:&quot;1,86&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590963,&quot;t&quot;:&quot;Real Oviedo&quot;,&quot;p&quot;:&quot;1,86&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073012,&quot;mi&quot;:252016,&quot;md&quot;:&quot;CD Tenerife: más/menos goles&quot;,&quot;rmd&quot;:&quot;CD Tenerife: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593426,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;3,22&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593427,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,33&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072976,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Real Oviedo: más/menos goles&quot;,&quot;rmd&quot;:&quot;Real Oviedo: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593169,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;3,22&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593170,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,30&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500899,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;0&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;CD Tenerife&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;1&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Real Oviedo&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305583,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Elche CF - Málaga&quot;,&quot;pi&quot;:30317947,&quot;pt&quot;:&quot;Elche - Málaga&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:75,&quot;b&quot;:[{&quot;i&quot;:1185072885,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591912,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;2,01&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591920,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;1,96&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591932,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;12,00&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073263,&quot;mi&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;rmd&quot;:&quot;Doble oportunidad&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869594669,&quot;t&quot;:&quot;1X&quot;,&quot;p&quot;:&quot;1,03&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594671,&quot;t&quot;:&quot;X2&quot;,&quot;p&quot;:&quot;1,61&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594670,&quot;t&quot;:&quot;12&quot;,&quot;p&quot;:&quot;1,66&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073213,&quot;mi&quot;:252028,&quot;md&quot;:&quot;Marcarán ambos equipos&quot;,&quot;rmd&quot;:&quot;Marcarán ambos equipos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869594366,&quot;t&quot;:&quot;Si&quot;,&quot;p&quot;:&quot;9,05&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869594367,&quot;t&quot;:&quot;No&quot;,&quot;p&quot;:&quot;1,03&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185179476,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869872266,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;1,66&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869872267,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;2,11&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073022,&quot;mi&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;rmd&quot;:&quot;Apuesta sin empate&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593246,&quot;t&quot;:&quot;Elche CF&quot;,&quot;p&quot;:&quot;1,10&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593250,&quot;t&quot;:&quot;Málaga&quot;,&quot;p&quot;:&quot;6,00&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185158541,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Elche CF: más/menos goles&quot;,&quot;rmd&quot;:&quot;Elche CF: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869812807,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;1,86&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869812808,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073478,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Málaga: más/menos goles&quot;,&quot;rmd&quot;:&quot;Málaga: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869595474,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;6,00&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869595479,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;1,12&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500901,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;9&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Elche CF&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;1&quot;,&quot;cn&quot;:&quot;1&quot;,&quot;r&quot;:[&quot;0&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Málaga&quot;,&quot;cr&quot;:&quot;0&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false},{&quot;i&quot;:30305585,&quot;di&quot;:1,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;ed&quot;:null,&quot;sdi&quot;:2,&quot;ei&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;t&quot;:&quot;Sporting - FC Cartagena&quot;,&quot;pi&quot;:30317951,&quot;pt&quot;:&quot;Sporting - Cartagena&quot;,&quot;hpb&quot;:false,&quot;ht&quot;:&quot;Segunda División&quot;,&quot;s&quot;:2,&quot;f&quot;:&quot;2025-05-25T18:30:00&quot;,&quot;h&quot;:&quot;18:30&quot;,&quot;st&quot;:&quot;&quot;,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;hv&quot;:0,&quot;nb&quot;:53,&quot;b&quot;:[{&quot;i&quot;:1185072653,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869590604,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,01&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590605,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;11,05&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869590606,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;36,00&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185072818,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869591736,&quot;t&quot;:&quot;+ de 4,5&quot;,&quot;p&quot;:&quot;1,63&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869591737,&quot;t&quot;:&quot;- de 4,5&quot;,&quot;p&quot;:&quot;2,16&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073226,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Sporting: más/menos goles&quot;,&quot;rmd&quot;:&quot;Sporting: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593934,&quot;t&quot;:&quot;+ de 3,5&quot;,&quot;p&quot;:&quot;2,06&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593935,&quot;t&quot;:&quot;- de 3,5&quot;,&quot;p&quot;:&quot;1,69&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185073177,&quot;mi&quot;:252018,&quot;md&quot;:&quot;FC Cartagena: más/menos goles&quot;,&quot;rmd&quot;:&quot;FC Cartagena: más/menos goles&quot;,&quot;l&quot;:true,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869593805,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;3,62&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869593807,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,25&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:true,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;si&quot;:9500903,&quot;sb&quot;:{&quot;sc&quot;:true,&quot;bt&quot;:false,&quot;po&quot;:&quot;&quot;,&quot;ty&quot;:&quot;FootballScoreboard&quot;,&quot;rt&quot;:-1,&quot;cpt&quot;:&quot;0&quot;,&quot;pm&quot;:&quot;72&quot;,&quot;pi&quot;:3,&quot;pd&quot;:&quot;2º Tiempo&quot;,&quot;tp&quot;:&quot;3&quot;,&quot;ep&quot;:&quot;&quot;,&quot;ct&quot;:&quot;&quot;,&quot;pt&quot;:[{&quot;yc&quot;:&quot;0&quot;,&quot;cn&quot;:&quot;3&quot;,&quot;r&quot;:[&quot;3&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;Sporting&quot;,&quot;cr&quot;:&quot;3&quot;,&quot;md&quot;:&quot;0&quot;},{&quot;yc&quot;:&quot;3&quot;,&quot;cn&quot;:&quot;2&quot;,&quot;r&quot;:[&quot;1&quot;],&quot;er&quot;:[],&quot;pr&quot;:[],&quot;e&quot;:&quot;0&quot;,&quot;rc&quot;:&quot;0&quot;,&quot;cl&quot;:null,&quot;ty&quot;:&quot;FootballParticipant&quot;,&quot;d&quot;:&quot;FC Cartagena&quot;,&quot;cr&quot;:&quot;1&quot;,&quot;md&quot;:&quot;0&quot;}],&quot;im&quot;:false},&quot;p&quot;:false,&quot;nsti&quot;:1,&quot;mp&quot;:false,&quot;pp&quot;:false,&quot;bbb&quot;:false,&quot;ih&quot;:false,&quot;ip&quot;:false}],&quot;subscription&quot;:{&quot;type&quot;:26,&quot;param&quot;:{&quot;sd&quot;:&quot;2&quot;,&quot;e&quot;:20,&quot;b&quot;:10,&quot;o&quot;:10,&quot;srd&quot;:false,&quot;sdd&quot;:[],&quot;sdp&quot;:null,&quot;smi&quot;:null}},&quot;visibleEvents&quot;:3,&quot;maxBetsToShowInARow&quot;:3,&quot;selectedOptions&quot;:[],&quot;wid&quot;:&quot;w_1-p_2-wt_68&quot;,&quot;resources&quot;:{&quot;moreOptions&quot;:&quot;Ver más opciones&quot;,&quot;noBetAvailable&quot;:&quot;En este momento no se permiten apuestas sobre este evento.&quot;,&quot;searchPlaceholder&quot;:&quot;Buscar por liga o torneo&quot;,&quot;liveLabel&quot;:&quot;Live&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;,&quot;interrupted&quot;:&quot;Interrumpido&quot;,&quot;showMore&quot;:&quot;Ver más&quot;,&quot;showLess&quot;:&quot;Ver menos&quot;},&quot;scoreboardTypeResources&quot;:{&quot;sres&quot;:{&quot;1&quot;:{&quot;scoreboardClass&quot;:&quot;mod_1&quot;,&quot;iconClass&quot;:&quot;mod-mod_1&quot;}}},&quot;filter&quot;:{&quot;disciplineFilter&quot;:[],&quot;promotedFilter&quot;:[],&quot;showStreaming&quot;:false},&quot;liveUrl&quot;:&quot;/live&quot;,&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>    <div data-jsfile="sportsbookSubdisciplineLiveEvents.widget.js?v=nFGsuxVKAotUeyeZKMfOr54hAA2bry0gZEX9pS7QroI" class="ljs" hidden="hidden"></div>



    <div hidden="" id="aw2-1" data-v="{&quot;SubdisciplineId&quot;:2,&quot;DisciplineId&quot;:1,&quot;NumberOfBets&quot;:10,&quot;NumberOfOptions&quot;:10,&quot;NumberOfEvents&quot;:0,&quot;NumberOfMarketsToShow&quot;:3,&quot;MaxEvents&quot;:20,&quot;VisibleEvents&quot;:3,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_1-p_2-wt_106_c" class="jqw  widget_type_106_c" data-wt="106" data-pa="2" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="4" data-nrc="0" data-ic="true" data-vtw="null" data-sn="SportsNoResult">




    <div class="jdata" data-section="sportsNoResult" data-hash="PyjtOZ-2gadSXfwTIK7Ws1oMsxHKC1aEOAT2tBYnb48"></div>


<div data-jsfile="sportsNoResult.section.js?v=PyjtOZ-2gadSXfwTIK7Ws1oMsxHKC1aEOAT2tBYnb48" class="ljs" hidden="hidden"></div>
    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw2-1" data-v="{&quot;ShowTitle&quot;:true,&quot;FromDiscipline&quot;:false,&quot;DisciplineId&quot;:1,&quot;FromCategory&quot;:false,&quot;CategoryId&quot;:null,&quot;FromSubdiscipline&quot;:true,&quot;SubdisciplineId&quot;:2,&quot;ParentHtmlId&quot;:&quot;w_1-p_2-wt_106_c&quot;,&quot;HtmlId&quot;:&quot;w_1-p_2-wt_106_c_SportsNoResult&quot;,&quot;ClassName&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_2-p_2-wt_43" class="jqw  widget_type_43" data-wt="43" data-pa="2" data-co="0" data-po="2" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="True" data-pwi="75" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">




<div class="headline headline--greyline headline--brandfont">
    <h2 class="title_m-l">
            Segunda División
    </h2>
</div>
<div hidden="" class="jwdata" data-d="Fútbol"></div>


    <div class="module__header-filters">
            <div class="widget__filter-offer mod_1">
                <ul class="tab__group">
                    <li class="tab__item tab__item--primary jtab active" data-i="2">
                        Eventos
                    </li>
                    <li class="tab__item tab__item--primary jtab " data-i="3">
                        Largo plazo
                    </li>
                </ul>
            </div>

            <div class="list-events__select-options">
                    <div class="jrm select-noform">
                        <div class="jsm select-noform_active" data-i="251961">
                            <span>1-X-2</span>
                            <i class="icon-chevron-thin-down jar"></i>
                        </div>
                        <ul class="none select-noform__options joml">
                                    <li class="jom" tabindex="0" data-i="252010">
                                        <span>Más/menos goles</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="251962">
                                        <span>Doble oportunidad</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="251966">
                                        <span>Apuesta sin empate</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252028">
                                        <span>Marcar ambos equipos</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252016">
                                        <span>Más/menos goles LOCAL</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252018">
                                        <span>Más/menos goles VISITANTE</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252071">
                                        <span>1º tiempo: 1-X-2</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252077">
                                        <span>1º tiempo: más/menos goles</span>
                                    </li>
                        </ul>
                    </div>
                    <div class="jrm select-noform">
                        <div class="jsm select-noform_active" data-i="252010">
                            <span>Más/menos goles</span>
                            <i class="icon-chevron-thin-down jar"></i>
                        </div>
                        <ul class="none select-noform__options joml">
                                    <li class="jom" tabindex="0" data-i="251961">
                                        <span>1-X-2</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="251962">
                                        <span>Doble oportunidad</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="251966">
                                        <span>Apuesta sin empate</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252028">
                                        <span>Marcar ambos equipos</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252016">
                                        <span>Más/menos goles LOCAL</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252018">
                                        <span>Más/menos goles VISITANTE</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252071">
                                        <span>1º tiempo: 1-X-2</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252077">
                                        <span>1º tiempo: más/menos goles</span>
                                    </li>
                        </ul>
                    </div>
                    <div class="jrm select-noform">
                        <div class="jsm select-noform_active" data-i="251962">
                            <span>Doble oportunidad</span>
                            <i class="icon-chevron-thin-down jar"></i>
                        </div>
                        <ul class="none select-noform__options joml">
                                    <li class="jom" tabindex="0" data-i="251961">
                                        <span>1-X-2</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252010">
                                        <span>Más/menos goles</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="251966">
                                        <span>Apuesta sin empate</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252028">
                                        <span>Marcar ambos equipos</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252016">
                                        <span>Más/menos goles LOCAL</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252018">
                                        <span>Más/menos goles VISITANTE</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252071">
                                        <span>1º tiempo: 1-X-2</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="252077">
                                        <span>1º tiempo: más/menos goles</span>
                                    </li>
                        </ul>
                    </div>
            </div>
    </div>



<article class="module__list-events">


<div id="react_0HNCR9FDERUPF"><div class="jsbdate"><div class="jtit accordion accordion_l "><h3 class="accordion__text">sábado, 31 de mayo de 2025</h3><div class=""></div><i class="ico-m icon-minus jshow" data-i="egd_0"></i></div><ul class="event__list jbgroup" data-i="egd_0"><li class="jlink jev event__item" data-u="/deportes/malaga-burgos-ev30430378" data-d="1" data-sdi="2" data-hv="0" data-il="0" data-i="30430378"><div class="event__tournament"></div><a href="/deportes/malaga-burgos-ev30430378" title="Málaga - Burgos" class="event__players"><ul class="event__players-name"><li>Málaga</li><li>Burgos</li></ul></a><div class="event__bets"><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869835274"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">2,09</span></li><li class="jo betbox" data-i="3869835275"><span class="jqt betbox__option">X</span><span class="jpr betbox__odd">3,10</span></li><li class="jo betbox" data-i="3869835276"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">3,84</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869836528"><span class="jqt betbox__option">+ de 1,5</span><span class="jpr betbox__odd">1,48</span></li><li class="jo betbox" data-i="3869836529"><span class="jqt betbox__option">- de 1,5</span><span class="jpr betbox__odd">2,52</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3869835269"><span class="jqt betbox__option">1X</span><span class="jpr betbox__odd">1,26</span></li><li class="jo betbox" data-i="3869835271"><span class="jqt betbox__option">X2</span><span class="jpr betbox__odd">1,68</span></li><li class="jo betbox" data-i="3869835270"><span class="jqt betbox__option">12</span><span class="jpr betbox__odd">1,36</span></li></ul></div></div><div class="event__more-info"><span class="event__day">31/05</span><span class="event__time">18:30</span><div class="event__tags"><span class="tag_rounded tag_rounded--outline tag_rounded--betbuilder">Crea tu apuesta</span></div></div><div class="jt_homemorebets event__more-bets jmr"><span>+29</span></div></li></ul></div></div><div hidden="" class="jcr" data-cid="react_0HNCR9FDERUPF" data-cn="$R.Jsx.s.sportsbookDate.SportsbookDateIndex" data-cp="{&quot;wid&quot;:&quot;w_2-p_2-wt_43&quot;,&quot;initialData&quot;:{&quot;e&quot;:[{&quot;i&quot;:30430378,&quot;d&quot;:&quot;Málaga - Burgos&quot;,&quot;di&quot;:1,&quot;sdi&quot;:2,&quot;dd&quot;:&quot;Fútbol&quot;,&quot;scd&quot;:null,&quot;sdd&quot;:&quot;Segunda División&quot;,&quot;ei&quot;:null,&quot;ed&quot;:null,&quot;du&quot;:&quot;2025-05-31T16:30:00Z&quot;,&quot;ds&quot;:&quot;31/05&quot;,&quot;lds&quot;:&quot;sábado, 31 de mayo de 2025&quot;,&quot;rd&quot;:0,&quot;ts&quot;:&quot;18:30&quot;,&quot;il&quot;:false,&quot;ns&quot;:true,&quot;pp&quot;:false,&quot;mp&quot;:false,&quot;bbb&quot;:true,&quot;hv&quot;:0,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;s&quot;:null,&quot;p&quot;:[{&quot;i&quot;:36895,&quot;n&quot;:&quot;Málaga&quot;,&quot;sn&quot;:&quot;MLG&quot;,&quot;t&quot;:2,&quot;h&quot;:true,&quot;p&quot;:null},{&quot;i&quot;:50932,&quot;n&quot;:&quot;Burgos&quot;,&quot;sn&quot;:&quot;BUR&quot;,&quot;t&quot;:3,&quot;h&quot;:false,&quot;p&quot;:null}],&quot;nb&quot;:30,&quot;ih&quot;:false,&quot;b&quot;:[{&quot;i&quot;:1185166794,&quot;mi&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;rmd&quot;:&quot;1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869835274,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;2,09&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869835275,&quot;t&quot;:&quot;X&quot;,&quot;p&quot;:&quot;3,10&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869835276,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;3,84&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185166792,&quot;mi&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;rmd&quot;:&quot;Doble oportunidad&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869835269,&quot;t&quot;:&quot;1X&quot;,&quot;p&quot;:&quot;1,26&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869835271,&quot;t&quot;:&quot;X2&quot;,&quot;p&quot;:&quot;1,68&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869835270,&quot;t&quot;:&quot;12&quot;,&quot;p&quot;:&quot;1,36&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167896,&quot;mi&quot;:252028,&quot;md&quot;:&quot;Marcarán ambos equipos&quot;,&quot;rmd&quot;:&quot;Marcarán ambos equipos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869837985,&quot;t&quot;:&quot;Si&quot;,&quot;p&quot;:&quot;2,17&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869837986,&quot;t&quot;:&quot;No&quot;,&quot;p&quot;:&quot;1,66&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167301,&quot;mi&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;rmd&quot;:&quot;Más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869836528,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;1,48&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869836529,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;2,52&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185166793,&quot;mi&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;rmd&quot;:&quot;Apuesta sin empate&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3869835272,&quot;t&quot;:&quot;Málaga&quot;,&quot;p&quot;:&quot;1,45&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869835273,&quot;t&quot;:&quot;Burgos&quot;,&quot;p&quot;:&quot;2,62&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167894,&quot;mi&quot;:252071,&quot;md&quot;:&quot;1º tiempo: 1-X-2&quot;,&quot;rmd&quot;:&quot;1º tiempo: 1-X-2&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869837971,&quot;t&quot;:&quot;Málaga&quot;,&quot;p&quot;:&quot;2,82&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869837972,&quot;t&quot;:&quot;Empate&quot;,&quot;p&quot;:&quot;1,96&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869837973,&quot;t&quot;:&quot;Burgos&quot;,&quot;p&quot;:&quot;4,64&quot;,&quot;d&quot;:3,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167907,&quot;mi&quot;:252077,&quot;md&quot;:&quot;1º tiempo: más/menos goles&quot;,&quot;rmd&quot;:&quot;1º tiempo: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869838014,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;1,56&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869838015,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;2,32&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167902,&quot;mi&quot;:252016,&quot;md&quot;:&quot;Málaga: más/menos goles&quot;,&quot;rmd&quot;:&quot;Málaga: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869838004,&quot;t&quot;:&quot;+ de 1,5&quot;,&quot;p&quot;:&quot;2,47&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869838005,&quot;t&quot;:&quot;- de 1,5&quot;,&quot;p&quot;:&quot;1,51&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1185167899,&quot;mi&quot;:252018,&quot;md&quot;:&quot;Burgos: más/menos goles&quot;,&quot;rmd&quot;:&quot;Burgos: más/menos goles&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:true,&quot;o&quot;:[[{&quot;i&quot;:3869837998,&quot;t&quot;:&quot;+ de 0,5&quot;,&quot;p&quot;:&quot;1,61&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3869837999,&quot;t&quot;:&quot;- de 0,5&quot;,&quot;p&quot;:&quot;2,17&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;mt&quot;:null,&quot;pt&quot;:null,&quot;pb&quot;:null,&quot;hcp&quot;:false,&quot;ctbg&quot;:null,&quot;bbtbg&quot;:null,&quot;si&quot;:0,&quot;sti&quot;:0,&quot;sb&quot;:null,&quot;cbl&quot;:true,&quot;ip&quot;:false}],&quot;m&quot;:[{&quot;i&quot;:251961,&quot;md&quot;:&quot;1-X-2&quot;,&quot;o&quot;:1},{&quot;i&quot;:252010,&quot;md&quot;:&quot;Más/menos goles&quot;,&quot;o&quot;:2},{&quot;i&quot;:251962,&quot;md&quot;:&quot;Doble oportunidad&quot;,&quot;o&quot;:3},{&quot;i&quot;:251966,&quot;md&quot;:&quot;Apuesta sin empate&quot;,&quot;o&quot;:4},{&quot;i&quot;:252028,&quot;md&quot;:&quot;Marcar ambos equipos&quot;,&quot;o&quot;:5},{&quot;i&quot;:252016,&quot;md&quot;:&quot;Más/menos goles LOCAL&quot;,&quot;o&quot;:8},{&quot;i&quot;:252018,&quot;md&quot;:&quot;Más/menos goles VISITANTE&quot;,&quot;o&quot;:9},{&quot;i&quot;:252071,&quot;md&quot;:&quot;1º tiempo: 1-X-2&quot;,&quot;o&quot;:12},{&quot;i&quot;:252077,&quot;md&quot;:&quot;1º tiempo: más/menos goles&quot;,&quot;o&quot;:13}]},&quot;disciplineId&quot;:1,&quot;resources&quot;:{&quot;mplus&quot;:&quot;Multi +&quot;,&quot;pplus&quot;:&quot;Player +&quot;,&quot;betBuilder&quot;:&quot;Crea tu apuesta&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;,&quot;rd1&quot;:&quot;Hoy&quot;,&quot;rd2&quot;:&quot;Mañana&quot;,&quot;ups&quot;:&quot;Ups&quot;,&quot;noResults&quot;:&quot;No se han encontrado resultados.&quot;,&quot;moreBets&quot;:&quot;Más apuestas&quot;,&quot;moreOptions&quot;:&quot;Ver más opciones&quot;},&quot;selectedOptionIds&quot;:[],&quot;numberOfMarkets&quot;:3,&quot;selectedMarketsIds&quot;:null,&quot;sportsUrl&quot;:&quot;/deportes&quot;,&quot;isEventTitleVisible&quot;:false,&quot;isEventDisciplineIconVisible&quot;:false,&quot;fromEncounter&quot;:false,&quot;betBuilderEnabled&quot;:true,&quot;maxOptionsPerBet&quot;:3,&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>    <div data-jsfile="sportsbookDate.section.js?v=QPr7o7VM8Y_cmKDfxSahqCh60fcI2qzXYlY3Rwc1ybg" class="ljs" hidden="hidden"></div>
</article>

<div data-jsfile="sportsbookSubdiscipline.widget.js?v=0eN63JXlgxlluqC2ZwYdfY-n1VI8RoYwDRapos9eoEI" class="ljs" hidden="hidden"></div>

    <div hidden="" id="aw2-2" data-v="{&quot;DisciplineId&quot;:1,&quot;SubdisciplineId&quot;:2,&quot;NumberOfBets&quot;:10,&quot;NumberOfEvents&quot;:0,&quot;OutrigthsNumberOfEvents&quot;:20,&quot;NumberOfOptions&quot;:10,&quot;NumberOfMarketsToShow&quot;:3,&quot;SelectedMarketsIds&quot;:null,&quot;SelectedTabId&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_3-p_2-wt_61" class="jqw  mkt_texts contentbox contentbox--radius-m widget_type_61" data-wt="61" data-pa="2" data-co="0" data-po="3" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="258" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">



        <div class="jhccollapse accordion accordion_m">
            <h1 class="accordion__text">Apostar a Segunda División ≫ RETAbet ES</h1>
            <i class="ico-m icon-chevron-small-up jicon"></i>
        </div>
    <div class="jhtmlcontent mkt_texts__content contentbox__content text_s-m" data-collapsed="false">
        <p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Si eres un apasionado del fútbol, en <strong>RETAbet</strong> puedes sumergirte en el emocionante mundo de las apuestas en <strong>Segunda División</strong>, también conocida como&nbsp;Hypermotion&nbsp;por razones de patrocinio. En estos emocionantes encuentros, la competencia alcanza su punto máximo, ya que cada partido es crucial y las oportunidades de ganar resultan verdaderamente emocionantes.</span></p>
<h2><p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><strong><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Apuestas en Segunda División o Liga Hypermotion</span></strong></p></h2>
<p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Las apuestas en Segunda División son perfectas para quienes buscan desafíos únicos. Todos los equipos compiten por ascender a <strong>Primera</strong> <strong>División</strong>, por lo que cada partido es intenso y está lleno de sorpresas. En RETAbet cuentas con diferentes opciones de apuestas en Segunda División, desde apostar a qué equipo será el próximo campeón de Segunda o quiénes ascenderán a <strong>LaLiga</strong>.</span></p>
<h2><p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><strong><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Palmarés en Segunda División&nbsp;</span></strong></p></h2>
<p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Esta liga está compuesta por 22 equipos, los cuales se disputan el ascenso a Primera División a lo largo de cerca de 450 partidos. Entre estos equipos destacan 8 por su palmarés de victorias:</span></p>
<ul style="list-style-type: disc; margin-left: 45.5px">
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Real Murcia</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 8 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Real Betis</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 7 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Deportivo de La Coruña</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 5 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Sporting de Gijón</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 5 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Real Oviedo</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 5 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Granada</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 4 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Osasuna</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">: 4 victorias</span></li>
    <li><strong><span style="font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Deportivo Alavés</span></strong><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">:&nbsp;4 victorias</span></li>
</ul>
<p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Muchos de ellos actualmente no se encuentran disputando la competición. O bien en LaLiga, o bien en <strong>Primera</strong> <strong>RFEF</strong>, la tercera categoría del fútbol español&nbsp;</span></p>
<h2><p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><strong><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Cuotas y pronósticos en Segunda División</span></strong></p></h2>
<p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">En nuestra página web encontrarás&nbsp;cuotas competitivas en cada partido&nbsp;y las herramientas de pronósticos que necesitas para tomar las mejores decisiones. Te recomendamos analizar las tendencias y el rendimiento de los equipos antes de apostar.</span></p>
<h2><p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><strong><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Cómo apostar en Segunda División</span></strong></p></h2>
<p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">¿Estás listo para apostar en Segunda División? ¡Adelante! Te contamos cómo, es muy sencillo. Para apostar solo tienes que <strong><a href="https://apuestas.retabet.es/registro"><span style="color: rgba(0, 0, 0, 1)">registrarte</span></a></strong> y realizar un depósito a través de cualquiera de los métodos de ingreso disponibles. Dirígete en el menú al apartado de <strong><a href="https://apuestas.retabet.es/deportes/futbol-m1"><span style="color: rgba(0, 0, 0, 1)">apuestas en fútbol</span></a></strong>, desde ahí selecciona la submodalidad de “Segunda División”. Aquí podrás escoger los partidos que más te gusten y comenzar tus apuestas en Segunda División.</span></p>
<h2><p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><strong><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">Apuestas de Fútbol online</span></strong></p></h2>
<p style="margin: 0 0 8pt; font-size: 11pt; font-family: " calibri",="" sans-serif;="" text-align:="" justify;="" line-height:="" normal"=""><span style="font-size: 11px; font-family: Poppins; color: rgba(0, 0, 0, 1)">En RETAbet, nuestra devoción por el fútbol trasciende los límites de la Segunda División. En nuestra plataforma, puedes realizar apuestas en una amplia gama de torneos y partidos. Desde la <strong><a href="https://apuestas.retabet.es/deportes/futbol/laliga-s1"><span style="color: rgba(0, 0, 0, 1)">LaLiga española</span></a></strong> hasta la emocionante atmósfera de la <strong><a href="https://apuestas.retabet.es/deportes/futbol/champions-league-s10"><span style="color: rgba(0, 0, 0, 1)">Champions League</span></a></strong> o la <strong><a href="https://apuestas.retabet.es/deportes/futbol/copa-del-rey-s5"><span style="color: rgba(0, 0, 0, 1)">Copa del Rey</span></a></strong>, encontrarás opciones que se adaptan a tus preferencias. Sumado a esto, puedes sumergirte en las emociones de la <strong><a href="https://apuestas.retabet.es/deportes/futbol/eurocopa-2024-s6823"><span style="color: rgba(0, 0, 0, 1)">Eurocopa</span></a></strong> y otras competiciones internacionales de renombre. ¿Te atrae la acción a nivel global? Explora las oportunidades internacionales apostando en ligas tan destacadas como la <strong><a href="https://apuestas.retabet.es/deportes/futbol/bundesliga-s8"><span style="color: rgba(0, 0, 0, 1)">Bundesliga</span></a></strong> , la prestigiosa <strong><a href="https://apuestas.retabet.es/deportes/futbol/premier-league-s6"><span style="color: rgba(0, 0, 0, 1)">Premier League</span></a></strong> o incluso participando en apuestas relacionadas con la<a href="https://apuestas.retabet.es/deportes/futbol/serie-a-s7"><span style="color: rgba(0, 0, 0, 1); text-decoration: none">&nbsp;</span><strong><span style="color: rgba(0, 0, 0, 1)">liga italiana</span></strong></a>. En RETAbet, no solamente celebramos la grandeza del fútbol, sino también las apasionantes oportunidades que el mundo de las apuestas online tiene para ofrecer.&nbsp;</span></p>
    </div>
    <div data-jsfile="htmlContent.widget.js?v=8iumHKsvzpx5Nf4oqTAjAnlt1ASnbTT__lTcL-iNhaA" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw2-3" data-v="{&quot;HtmlContentId&quot;:0,&quot;ClassName&quot;:&quot;mkt_texts contentbox contentbox--radius-m&quot;,&quot;DisciplineId&quot;:1,&quot;SubdisciplineId&quot;:2,&quot;TitleVisible&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
    <section data-cont="3" class="jpanel panel__betslip">


    <section id="w_1-p_3-wt_6" class="jqw  widget_type_6" data-wt="6" data-pa="3" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="76" data-nrc="1" data-ic="false" data-vtw="null" data-sn="">




    <div class="video jstreamingContainer jactiveStreaming" data-active="True" data-unpinone="False" data-sc="30406729" data-sbu="False">


    <div class="video__content jcontwr " data-pex="0" data-min="0">

        <div class="jvideoSection " data-ty="2" data-sc="30406729" data-sec="pse">

                <div class="str__control_bar">
<div id="react_0HNCR9FDERUPG"><div tabindex="0"><i class="jlistArr ico-s icon-reorder"></i><i class="ico-s mod-mod_8"></i><div><span class="str__list_item active"> <!-- -->E. Nava - B. Van De Zandschulp</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div><ul class="str__list none jlistCont"><li data-sc="30398643" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_5"></i><span>As Mónaco - Fenerbahce</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30409852" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>AZ Alkmaar - FC Twente</span></div></li><li data-sc="30305416" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Spezia - Catanzaro</span></div></li><li data-sc="30409847" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Audace Cerignola - Pescara</span></div></li><li data-sc="30409849" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Vicenza - Ternana</span></div></li><li data-sc="30373317" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Union Saint-Gilloise - Gent</span></div></li><li data-sc="30373319" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Club Brujas - Amberes</span></div></li><li data-sc="30373321" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Genk - Anderlecht</span></div></li><li data-sc="30410361" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Nsi Runavik - Hb Torshavn</span></div></li><li data-sc="30410398" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FC Botev Vratsa - Slavia Sofia</span></div></li><li data-sc="30410067" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FC Gareji - FC Iberia 1999</span></div></li><li data-sc="30305749" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Colegiales - CD Maipu</span></div></li><li data-sc="30410471" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Berazategui - Jj Urquiza</span></div></li><li data-sc="30424957" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Botafogo Pb - Retro FC Brasil</span></div></li><li data-sc="30305183" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Ñublense - O'higgins</span></div></li><li data-sc="30305592" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Libertad FC - Deportivo Macara</span></div></li><li data-sc="30410088" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Ajman - Al-Khaleej Khor Fakkan</span></div></li><li data-sc="30410275" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Haugesund - Brann</span></div></li><li data-sc="30305594" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Asociacion Deportiva Tarma - Ayacucho FC</span></div></li><li data-sc="30353934" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FK Partizan - Vojvodina</span></div></li><li data-sc="30353935" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FK Radnicki 1923 - Tsc Backa Topola</span></div></li><li data-sc="30353937" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Ofk Beograd - FK Novi Pazar</span></div></li><li data-sc="30406610" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>J. Paolini - Y. Yuan</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406640" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>D. Vekic - A. Blinkova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30398981" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>N. Stojanovic - A. Anisimova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406664" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>I. Jovic - R. Zarazua</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406633" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>O. Danilovic - L. Fernandez</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406615" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>A. Potapova - L. Noskova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406562" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>M. Kostyuk - S. Bejlek</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30398878" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_5"></i><span>Reyer Venecia - Virtus Bologna</span></div></li><li data-sc="30371187" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_5"></i><span>Kk Split - Kk Dinamo Zagreb</span></div></li><li data-sc="30414635" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>J. Tichy - R. Merkl</span></div></li><li data-sc="30414846" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>Andrii Regush - V. Korobko</span></div></li><li data-sc="30414947" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>A. Sydorenko - H. Buianover</span></div></li><li data-sc="30414445" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>I. Todiras - I. Uzun</span></div></li><li data-sc="30414473" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>Jan Seeman - Filip Kubos</span></div></li><li data-sc="30414485" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>S. Yureneva - O. Yureneva</span></div></li><li data-sc="30412788" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Wolves (lzrn) - Tottenham Hotspur (aguuero)</span></div></li><li data-sc="30413318" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Brighton (Cofardi) - Leicester (Linox)</span></div></li><li data-sc="30412233" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Bayer 04 Leverkusen (Koss) - Borussia Dortmund (Fireball)</span></div></li><li data-sc="30412518" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Eintracht Frankfurt (Sheva) - RB Leipzig (Profik)</span></div></li><li data-sc="30430419" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Real Madrid (DIVINE) - Paris SG (FORCE)</span></div></li><li data-sc="30430449" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>England (THREAT) - Spain (POWER)</span></div></li><li data-sc="30430452" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Arsenal (BLITZ) - Aston Villa (GRIMACE)</span></div></li><li data-sc="30430783" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Flamengo (Eliot) - Boca Juniors (Blake)</span></div></li><li data-sc="30430742" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Manchester City (Rose) - Spurs (Megan)</span></div></li><li data-sc="30412056" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Houston Rockets (Pakapaka) - Phoenix Suns (Jovke)</span></div></li><li data-sc="30430658" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Boston Celtics (Sparkz) - Oklahoma City Thunder (CHIEF)</span></div></li><li data-sc="30430661" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Miami Heat (CALAMITY) - Toronto Raptors (CRUCIAL)</span></div></li><li data-sc="30430756" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Golden State Warriors (Tommy) - Brooklyn Nets (Donovan)</span></div></li><li data-sc="30413440" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Winnipeg Jets (Wryi) - Dallas Stars (OneUniq)</span></div></li><li data-sc="30409757" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_104"></i><span>M. Zakaria - T. Momen</span></div></li><li data-sc="c1747526412212071" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_27"></i><span>Carreras 24 h</span></div></li><li data-sc="c1747526414893670" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_28"></i><span>Carreras 24 h</span></div></li></ul></div></div><div hidden="" class="jcr" data-cid="react_0HNCR9FDERUPG" data-cn="$R.Jsx.s.streaming.StreamingEventList" data-cp="{&quot;initialData&quot;:{&quot;e&quot;:[{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406729&quot;,&quot;t&quot;:&quot;E. Nava - B. Van De Zandschulp&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Masculino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30398643&quot;,&quot;t&quot;:&quot;As Mónaco - Fenerbahce&quot;,&quot;ic&quot;:&quot;5&quot;,&quot;st&quot;:&quot;Euroliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409852&quot;,&quot;t&quot;:&quot;AZ Alkmaar - FC Twente&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Países Bajos Eredivisie - Eliminatorias&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305416&quot;,&quot;t&quot;:&quot;Spezia - Catanzaro&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Italia Serie B&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409847&quot;,&quot;t&quot;:&quot;Audace Cerignola - Pescara&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Italia Serie C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409849&quot;,&quot;t&quot;:&quot;Vicenza - Ternana&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Italia Serie C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30373317&quot;,&quot;t&quot;:&quot;Union Saint-Gilloise - Gent&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bélgica 1A Pro League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30373319&quot;,&quot;t&quot;:&quot;Club Brujas - Amberes&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bélgica 1A Pro League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30373321&quot;,&quot;t&quot;:&quot;Genk - Anderlecht&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bélgica 1A Pro League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410361&quot;,&quot;t&quot;:&quot;Nsi Runavik - Hb Torshavn&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Islas Feroe Premier League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410398&quot;,&quot;t&quot;:&quot;FC Botev Vratsa - Slavia Sofia&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bulgaria Parva Liga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410067&quot;,&quot;t&quot;:&quot;FC Gareji - FC Iberia 1999&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Georgia Erovnuli Liga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305749&quot;,&quot;t&quot;:&quot;Colegiales - CD Maipu&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Argentina Primera Nacional&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410471&quot;,&quot;t&quot;:&quot;Berazategui - Jj Urquiza&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Argentina Primera C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30424957&quot;,&quot;t&quot;:&quot;Botafogo Pb - Retro FC Brasil&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Brasil Serie C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305183&quot;,&quot;t&quot;:&quot;Ñublense - O\u0027higgins&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Chile Primera División&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305592&quot;,&quot;t&quot;:&quot;Libertad FC - Deportivo Macara&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Ecuador Serie A&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410088&quot;,&quot;t&quot;:&quot;Ajman - Al-Khaleej Khor Fakkan&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;EAU Arabian Gulf League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410275&quot;,&quot;t&quot;:&quot;Haugesund - Brann&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Noruega Eliteserien&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305594&quot;,&quot;t&quot;:&quot;Asociacion Deportiva Tarma - Ayacucho FC&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Perú Liga 1&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30353934&quot;,&quot;t&quot;:&quot;FK Partizan - Vojvodina&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Serbia Superliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30353935&quot;,&quot;t&quot;:&quot;FK Radnicki 1923 - Tsc Backa Topola&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Serbia Superliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30353937&quot;,&quot;t&quot;:&quot;Ofk Beograd - FK Novi Pazar&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Serbia Superliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406610&quot;,&quot;t&quot;:&quot;J. Paolini - Y. Yuan&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406640&quot;,&quot;t&quot;:&quot;D. Vekic - A. Blinkova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30398981&quot;,&quot;t&quot;:&quot;N. Stojanovic - A. Anisimova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406664&quot;,&quot;t&quot;:&quot;I. Jovic - R. Zarazua&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406633&quot;,&quot;t&quot;:&quot;O. Danilovic - L. Fernandez&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406615&quot;,&quot;t&quot;:&quot;A. Potapova - L. Noskova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406562&quot;,&quot;t&quot;:&quot;M. Kostyuk - S. Bejlek&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30398878&quot;,&quot;t&quot;:&quot;Reyer Venecia - Virtus Bologna&quot;,&quot;ic&quot;:&quot;5&quot;,&quot;st&quot;:&quot;Italia Lega Basket Serie A&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30371187&quot;,&quot;t&quot;:&quot;Kk Split - Kk Dinamo Zagreb&quot;,&quot;ic&quot;:&quot;5&quot;,&quot;st&quot;:&quot;Croacia Premijer Liga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414635&quot;,&quot;t&quot;:&quot;J. Tichy - R. Merkl&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414846&quot;,&quot;t&quot;:&quot;Andrii Regush - V. Korobko&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414947&quot;,&quot;t&quot;:&quot;A. Sydorenko - H. Buianover&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414445&quot;,&quot;t&quot;:&quot;I. Todiras - I. Uzun&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414473&quot;,&quot;t&quot;:&quot;Jan Seeman - Filip Kubos&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414485&quot;,&quot;t&quot;:&quot;S. Yureneva - O. Yureneva&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Femenina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412788&quot;,&quot;t&quot;:&quot;Wolves (lzrn) - Tottenham Hotspur (aguuero)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - FA Cup Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30413318&quot;,&quot;t&quot;:&quot;Brighton (Cofardi) - Leicester (Linox)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - FA Cup Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412233&quot;,&quot;t&quot;:&quot;Bayer 04 Leverkusen (Koss) - Borussia Dortmund (Fireball)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta Bundesliga Battle - 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412518&quot;,&quot;t&quot;:&quot;Eintracht Frankfurt (Sheva) - RB Leipzig (Profik)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta Bundesliga Battle - 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430419&quot;,&quot;t&quot;:&quot;Real Madrid (DIVINE) - Paris SG (FORCE)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430449&quot;,&quot;t&quot;:&quot;England (THREAT) - Spain (POWER)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430452&quot;,&quot;t&quot;:&quot;Arsenal (BLITZ) - Aston Villa (GRIMACE)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430783&quot;,&quot;t&quot;:&quot;Flamengo (Eliot) - Boca Juniors (Blake)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430742&quot;,&quot;t&quot;:&quot;Manchester City (Rose) - Spurs (Megan)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valkiria Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412056&quot;,&quot;t&quot;:&quot;Houston Rockets (Pakapaka) - Phoenix Suns (Jovke)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - NBA Battle - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430658&quot;,&quot;t&quot;:&quot;Boston Celtics (Sparkz) - Oklahoma City Thunder (CHIEF)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430661&quot;,&quot;t&quot;:&quot;Miami Heat (CALAMITY) - Toronto Raptors (CRUCIAL)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430756&quot;,&quot;t&quot;:&quot;Golden State Warriors (Tommy) - Brooklyn Nets (Donovan)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - Valhalla League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30413440&quot;,&quot;t&quot;:&quot;Winnipeg Jets (Wryi) - Dallas Stars (OneUniq)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ehockey - NHL Western Conference Battle - 3x4 mins&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409757&quot;,&quot;t&quot;:&quot;M. Zakaria - T. Momen&quot;,&quot;ic&quot;:&quot;104&quot;,&quot;st&quot;:&quot;Open de Palm Hills Masculino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;es&quot;:null,&quot;t&quot;:null,&quot;l&quot;:[{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1747526412212071&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;27&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1747526414893670&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;28&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;ine&quot;:false,&quot;hml&quot;:true},&quot;subscription&quot;:{&quot;type&quot;:14,&quot;param&quot;:{&quot;sdd&quot;:[],&quot;ste&quot;:[1],&quot;spe&quot;:null,&quot;cc&quot;:&quot;ES&quot;,&quot;ec&quot;:[&quot;3 W\u0026B&quot;,&quot;6 W\u0026B&quot;]}},&quot;wid&quot;:&quot;w_1-p_3-wt_6&quot;,&quot;selectedEvent&quot;:{&quot;sec&quot;:&quot;pse&quot;,&quot;ty&quot;:2,&quot;c&quot;:&quot;30406729&quot;,&quot;t&quot;:&quot;E. Nava - B. Van De Zandschulp&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Masculino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},&quot;hasVideoSelector&quot;:true,&quot;resources&quot;:{&quot;greyhounds&quot;:&quot;Galgos&quot;,&quot;horses&quot;:&quot;Caballos&quot;,&quot;greyhoundsAndHorses&quot;:&quot;Carreras 24 h&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;},&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>
                    <ul class="str__controls jstroplst">

                            <li data-t="4" class="str__control_item jstropt none">
                                <i class="ico-s icon-expand"></i>
                            </li>
                            <li data-t="5" class="str__control_item jstropt ">
                                <i class="ico-s icon-contract"></i>
                            </li>

                                <li data-t="2" class="str__control_item jstropt jpinunpin">
                                    <i class="ico-s icon-pin"></i>
                                </li>


                    </ul>
                </div>
                <div class="play jplayerWrapper" data-pt="1">




    <div id="video" class="jintPlayer none" data-pt="1" data-pid="1" data-src="" data-prot="1" data-apiurl="https://api.livestreaming.imgarena.com/api/v2/streaming/events/486240/stream?operatorId=25&amp;auth=0c92563f5e233858479c048ee67517c1&amp;timestamp=1748196242769&amp;page.page=1&amp;page.size=1" data-apihead="null" data-an="UA-34961270-1" data-drm="">

    <script src="/js/video.js?v=cgtYl4qcGXYRWYqGwa16sWUVoL1Gml9DOfVHMaQMUJw"></script>
    <div id="videocontainer">
        <video class="jshakaplayer vjs-fluid" disableremoteplayback="" autoplay="" muted="muted">
        </video>
    </div>

    </div>

                    <p class="play_no_str__text jnovid none">
                        <span>
                            en este momento no hay video disponible
                        </span>
                    </p>
                </div>

                <a href="/live/e-nava-b-van-de-zandschulp-sc30406729" class="str__bets-link jlink" title="E. Nava - B. Van De Zandschulp">
                    Ver apuestas
                    <i class="ico-s icon__bold icon-chevron-thin-right"></i>
                </a>
        </div>
    </div>
    <div id="login" class="jstPrEnded widget__login_bg none">

        <div class="widget__login">
            <a class="btn btn-m btn__contrast-outline jlb jt_streamingLog">
                Entrar a mi cuenta
            </a>
            <span class="widget__login_footer-links">
                <a class="widget__login_text_button jlink jt_streamingReg">
                    Quiero registrarme
                    <i class="icon-text-arrow-right icon__bold"></i>
                </a>
            </span>
        </div>
    </div>
    <div data-jsfile="streaming.section.js?v=K9IXm3CDCeY7V2LPCt0n_uqSLa0Rayyp5b57q8Lt-Xk" class="ljs" hidden="hidden"></div>

    </div>
    <div data-jsfile="streaming.widget.js?v=y6DsDbtcBFroCKpeEqKty8uFmvFPmuNsaRhIDA1X26c" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw3-1" data-v="{&quot;QueryStringEventId&quot;:0,&quot;IsPinUnpinEnabled&quot;:true,&quot;HasMinimizeMagnifyOption&quot;:false,&quot;IsOnlyActiveInUnpinnedMode&quot;:false,&quot;HasVideoSelector&quot;:true,&quot;HasScrollTopButton&quot;:false,&quot;DoesShowBetsLinkBar&quot;:true,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_4-p_3-wt_55" class="jqw  mod_28 widget_type_55" data-wt="55" data-pa="3" data-co="0" data-po="4" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="141" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">



    <div class="jgg contentbox contentbox--radius-m games-casino__home" data-flu="">
        <div class="jgcl accordion accordion_m">
            <h2 class="accordion__text">
                Juegos casino
            </h2>
            <i class="jgcli ico-m icon-chevron-up"></i>
        </div>
        <div class="jgl contentbox__content">
            <ul class="games__list-home">
                    <li class="jt_casGame jgm game__item ">

                        <div class="game__img">
                            <picture>
                                <img src="https://cdn.retabet.es/apuestas/es/CasinoGames/halloween_fortune_6.jpg">
                            </picture>
                        </div>

                        <span class="game__name jgn">Halloween Fortune</span>



                        <div class="game__buttons jgm jgmb" data-gt="gpas_hfortune_pop" data-ct="ngm_desktop" data-gtt="AZA" data-n="Halloween Fortune" data-pid="1" data-url="/halloween-fortune-cg-p1-igpas_hfortune_pop" data-ccd="0" data-sic="ico-xs" data-slic="ico-s" data-cm="real">
                                    <button class="btn btn-m btn__casino">
                                        JUGAR
                                    </button>
                        </div>
                    </li>
                    <li class="jt_casGame jgm game__item ">

                        <div class="game__img">
                            <picture>
                                <img src="https://cdn.retabet.es/apuestas/es/CasinoGames/FEED_OInk_Oink_Oink.jpg">
                            </picture>
                        </div>

                        <span class="game__name jgn">Oink Oink Oink</span>



                        <div class="game__buttons jgm jgmb" data-gt="gpas_oinka1_pop" data-ct="ngm_desktop" data-gtt="AZA" data-n="Oink Oink Oink" data-pid="1" data-url="/oink-oink-oink-cg-p1-igpas_oinka1_pop" data-ccd="0" data-sic="ico-xs" data-slic="ico-s" data-cm="real">
                                    <button class="btn btn-m btn__casino">
                                        JUGAR
                                    </button>
                        </div>
                    </li>
                    <li class="jt_casGame jgm game__item ">

                        <div class="game__img">
                            <picture>
                                <img src="https://cdn.retabet.es/apuestas/es/CasinoGames/FEED_Big_Circus.jpg">
                            </picture>
                        </div>

                        <span class="game__name jgn">BIG CIRCUS </span>



                        <div class="game__buttons jgm jgmb" data-gt="gpas_bcircuslo_pop" data-ct="ngm_desktop" data-gtt="AZA" data-n="BIG CIRCUS " data-pid="1" data-url="/big-circus-cg-p1-igpas_bcircuslo_pop" data-ccd="0" data-sic="ico-xs" data-slic="ico-s" data-cm="real">
                                    <button class="btn btn-m btn__casino">
                                        JUGAR
                                    </button>
                        </div>
                    </li>
                    <li class="jt_casGame jgm game__item ">

                        <div class="game__img">
                            <picture>
                                <img src="https://cdn.retabet.es/apuestas/es/CasinoGames/NL_dragon_bonanza.jpg">
                            </picture>
                        </div>

                        <span class="game__name jgn">Dragon Bonanza</span>



                        <div class="game__buttons jgm jgmb" data-gt="gpas_goldhit3_pop" data-ct="ngm_desktop" data-gtt="AZA" data-n="Dragon Bonanza" data-pid="1" data-url="/dragon-bonanza-cg-p1-igpas_goldhit3_pop" data-ccd="0" data-sic="ico-xs" data-slic="ico-s" data-cm="real">
                                    <button class="btn btn-m btn__casino">
                                        JUGAR
                                    </button>
                        </div>
                    </li>
                    <li class="jt_casGame jgm game__item ">

                        <div class="game__img">
                            <picture>
                                <img src="https://cdn.retabet.es/apuestas/es/CasinoGames/piggies_and_the_bank_0.jpg">
                            </picture>
                        </div>

                        <span class="game__name jgn">Piggies and The Bank</span>



                        <div class="game__buttons jgm jgmb" data-gt="gpas_engageb1_pop" data-ct="ngm_desktop" data-gtt="AZA" data-n="Piggies and The Bank" data-pid="1" data-url="/piggies-and-the-bank-cg-p1-igpas_engageb1_pop" data-ccd="0" data-sic="ico-xs" data-slic="ico-s" data-cm="real">
                                    <button class="btn btn-m btn__casino">
                                        JUGAR
                                    </button>
                        </div>
                    </li>
                    <li class="jt_casGame jgm game__item ">

                        <div class="game__img">
                            <picture>
                                <img src="https://cdn.retabet.es/apuestas/es/CasinoGames/FEED_Wild_Pistolero.jpg">
                            </picture>
                        </div>

                        <span class="game__name jgn">Wild Pistolero</span>



                        <div class="game__buttons jgm jgmb" data-gt="gpas_wpistolo_pop" data-ct="ngm_desktop" data-gtt="AZA" data-n="Wild Pistolero" data-pid="1" data-url="/wild-pistolero-cg-p1-igpas_wpistolo_pop" data-ccd="0" data-sic="ico-xs" data-slic="ico-s" data-cm="real">
                                    <button class="btn btn-m btn__casino">
                                        JUGAR
                                    </button>
                        </div>
                    </li>
            </ul>
        </div>
    </div>
    <div data-jsfile="quickGames.widget.js?v=HmlVpIfddkyYOkgAMPcyLlgAY_7yKDdSOXPCbhmoEUc" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw3-4" data-v="{&quot;NumGames&quot;:6,&quot;ProviderId&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
    <section data-cont="4" class="jpanel floatbetslip__panel">


    <section id="w_1-p_4-wt_6" class="jqw  none widget_type_6" data-wt="6" data-pa="4" data-co="0" data-po="1" data-sw="false" data-vi="False" data-sl="True" data-ti="False" data-sc="False" data-pwi="180" data-nrc="1" data-ic="false" data-vtw="null" data-sn="">




    <div class="video jstreamingContainer " data-active="False" data-unpinone="True" data-sc="30406729" data-sbu="False">


    <div class="video__content jcontwr " data-pex="0" data-min="0">

            <div class="video__collapsedheader jcollapseHeaderSection none">
                <div tabindex="0" class="jminTabCont" data-reactroot="">
                    <i class="mod-mod_8"></i>
                    <span class="jminTab str__list_item active">E. Nava - B. Van De Zandschulp</span>

                    <span class=" tag_streaming tag_streaming--prime">
                        <i class="icon-youtube-play"></i>
                            Prime
                    </span>
                </div>
                <i class="icon-chevron-up jholdup"></i>
            </div>
        <div class="jvideoSection " data-ty="2" data-sc="30406729" data-sec="pse">

                <div class="str__control_bar">
<div id="react_0HNCR9FDERUPC"><div tabindex="0"><i class="jlistArr ico-s icon-reorder"></i><i class="ico-s mod-mod_8"></i><div><span class="str__list_item active"> <!-- -->E. Nava - B. Van De Zandschulp</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div><ul class="str__list none jlistCont"><li data-sc="30398643" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_5"></i><span>As Mónaco - Fenerbahce</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30409852" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>AZ Alkmaar - FC Twente</span></div></li><li data-sc="30305416" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Spezia - Catanzaro</span></div></li><li data-sc="30409847" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Audace Cerignola - Pescara</span></div></li><li data-sc="30409849" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Vicenza - Ternana</span></div></li><li data-sc="30373317" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Union Saint-Gilloise - Gent</span></div></li><li data-sc="30373319" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Club Brujas - Amberes</span></div></li><li data-sc="30373321" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Genk - Anderlecht</span></div></li><li data-sc="30410361" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Nsi Runavik - Hb Torshavn</span></div></li><li data-sc="30410398" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FC Botev Vratsa - Slavia Sofia</span></div></li><li data-sc="30410067" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FC Gareji - FC Iberia 1999</span></div></li><li data-sc="30305749" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Colegiales - CD Maipu</span></div></li><li data-sc="30410471" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Berazategui - Jj Urquiza</span></div></li><li data-sc="30424957" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Botafogo Pb - Retro FC Brasil</span></div></li><li data-sc="30305183" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Ñublense - O'higgins</span></div></li><li data-sc="30305592" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Libertad FC - Deportivo Macara</span></div></li><li data-sc="30410088" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Ajman - Al-Khaleej Khor Fakkan</span></div></li><li data-sc="30410275" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Haugesund - Brann</span></div></li><li data-sc="30305594" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Asociacion Deportiva Tarma - Ayacucho FC</span></div></li><li data-sc="30353934" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FK Partizan - Vojvodina</span></div></li><li data-sc="30353935" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>FK Radnicki 1923 - Tsc Backa Topola</span></div></li><li data-sc="30353937" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Ofk Beograd - FK Novi Pazar</span></div></li><li data-sc="30406610" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>J. Paolini - Y. Yuan</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406640" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>D. Vekic - A. Blinkova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30398981" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>N. Stojanovic - A. Anisimova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406664" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>I. Jovic - R. Zarazua</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406633" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>O. Danilovic - L. Fernandez</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406615" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>A. Potapova - L. Noskova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30406562" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>M. Kostyuk - S. Bejlek</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div></li><li data-sc="30398878" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_5"></i><span>Reyer Venecia - Virtus Bologna</span></div></li><li data-sc="30371187" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_5"></i><span>Kk Split - Kk Dinamo Zagreb</span></div></li><li data-sc="30414635" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>J. Tichy - R. Merkl</span></div></li><li data-sc="30414846" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>Andrii Regush - V. Korobko</span></div></li><li data-sc="30414947" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>A. Sydorenko - H. Buianover</span></div></li><li data-sc="30414445" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>I. Todiras - I. Uzun</span></div></li><li data-sc="30414473" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>Jan Seeman - Filip Kubos</span></div></li><li data-sc="30414485" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>S. Yureneva - O. Yureneva</span></div></li><li data-sc="30412788" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Wolves (lzrn) - Tottenham Hotspur (aguuero)</span></div></li><li data-sc="30413318" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Brighton (Cofardi) - Leicester (Linox)</span></div></li><li data-sc="30412233" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Bayer 04 Leverkusen (Koss) - Borussia Dortmund (Fireball)</span></div></li><li data-sc="30412518" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Eintracht Frankfurt (Sheva) - RB Leipzig (Profik)</span></div></li><li data-sc="30430419" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Real Madrid (DIVINE) - Paris SG (FORCE)</span></div></li><li data-sc="30430449" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>England (THREAT) - Spain (POWER)</span></div></li><li data-sc="30430452" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Arsenal (BLITZ) - Aston Villa (GRIMACE)</span></div></li><li data-sc="30430783" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Flamengo (Eliot) - Boca Juniors (Blake)</span></div></li><li data-sc="30430742" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Manchester City (Rose) - Spurs (Megan)</span></div></li><li data-sc="30412056" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Houston Rockets (Pakapaka) - Phoenix Suns (Jovke)</span></div></li><li data-sc="30430658" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Boston Celtics (Sparkz) - Oklahoma City Thunder (CHIEF)</span></div></li><li data-sc="30430661" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Miami Heat (CALAMITY) - Toronto Raptors (CRUCIAL)</span></div></li><li data-sc="30430756" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Golden State Warriors (Tommy) - Brooklyn Nets (Donovan)</span></div></li><li data-sc="30413440" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Winnipeg Jets (Wryi) - Dallas Stars (OneUniq)</span></div></li><li data-sc="30409757" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_104"></i><span>M. Zakaria - T. Momen</span></div></li><li data-sc="c1747526412212071" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_27"></i><span>Carreras 24 h</span></div></li><li data-sc="c1747526414893670" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_28"></i><span>Carreras 24 h</span></div></li></ul></div></div><div hidden="" class="jcr" data-cid="react_0HNCR9FDERUPC" data-cn="$R.Jsx.s.streaming.StreamingEventList" data-cp="{&quot;initialData&quot;:{&quot;e&quot;:[{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406729&quot;,&quot;t&quot;:&quot;E. Nava - B. Van De Zandschulp&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Masculino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30398643&quot;,&quot;t&quot;:&quot;As Mónaco - Fenerbahce&quot;,&quot;ic&quot;:&quot;5&quot;,&quot;st&quot;:&quot;Euroliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409852&quot;,&quot;t&quot;:&quot;AZ Alkmaar - FC Twente&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Países Bajos Eredivisie - Eliminatorias&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305416&quot;,&quot;t&quot;:&quot;Spezia - Catanzaro&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Italia Serie B&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409847&quot;,&quot;t&quot;:&quot;Audace Cerignola - Pescara&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Italia Serie C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409849&quot;,&quot;t&quot;:&quot;Vicenza - Ternana&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Italia Serie C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30373317&quot;,&quot;t&quot;:&quot;Union Saint-Gilloise - Gent&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bélgica 1A Pro League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30373319&quot;,&quot;t&quot;:&quot;Club Brujas - Amberes&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bélgica 1A Pro League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30373321&quot;,&quot;t&quot;:&quot;Genk - Anderlecht&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bélgica 1A Pro League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410361&quot;,&quot;t&quot;:&quot;Nsi Runavik - Hb Torshavn&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Islas Feroe Premier League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410398&quot;,&quot;t&quot;:&quot;FC Botev Vratsa - Slavia Sofia&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Bulgaria Parva Liga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410067&quot;,&quot;t&quot;:&quot;FC Gareji - FC Iberia 1999&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Georgia Erovnuli Liga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305749&quot;,&quot;t&quot;:&quot;Colegiales - CD Maipu&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Argentina Primera Nacional&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410471&quot;,&quot;t&quot;:&quot;Berazategui - Jj Urquiza&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Argentina Primera C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30424957&quot;,&quot;t&quot;:&quot;Botafogo Pb - Retro FC Brasil&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Brasil Serie C&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305183&quot;,&quot;t&quot;:&quot;Ñublense - O\u0027higgins&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Chile Primera División&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305592&quot;,&quot;t&quot;:&quot;Libertad FC - Deportivo Macara&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Ecuador Serie A&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410088&quot;,&quot;t&quot;:&quot;Ajman - Al-Khaleej Khor Fakkan&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;EAU Arabian Gulf League&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30410275&quot;,&quot;t&quot;:&quot;Haugesund - Brann&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Noruega Eliteserien&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30305594&quot;,&quot;t&quot;:&quot;Asociacion Deportiva Tarma - Ayacucho FC&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Perú Liga 1&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30353934&quot;,&quot;t&quot;:&quot;FK Partizan - Vojvodina&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Serbia Superliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30353935&quot;,&quot;t&quot;:&quot;FK Radnicki 1923 - Tsc Backa Topola&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Serbia Superliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30353937&quot;,&quot;t&quot;:&quot;Ofk Beograd - FK Novi Pazar&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Serbia Superliga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406610&quot;,&quot;t&quot;:&quot;J. Paolini - Y. Yuan&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406640&quot;,&quot;t&quot;:&quot;D. Vekic - A. Blinkova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30398981&quot;,&quot;t&quot;:&quot;N. Stojanovic - A. Anisimova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406664&quot;,&quot;t&quot;:&quot;I. Jovic - R. Zarazua&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406633&quot;,&quot;t&quot;:&quot;O. Danilovic - L. Fernandez&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406615&quot;,&quot;t&quot;:&quot;A. Potapova - L. Noskova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30406562&quot;,&quot;t&quot;:&quot;M. Kostyuk - S. Bejlek&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30398878&quot;,&quot;t&quot;:&quot;Reyer Venecia - Virtus Bologna&quot;,&quot;ic&quot;:&quot;5&quot;,&quot;st&quot;:&quot;Italia Lega Basket Serie A&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30371187&quot;,&quot;t&quot;:&quot;Kk Split - Kk Dinamo Zagreb&quot;,&quot;ic&quot;:&quot;5&quot;,&quot;st&quot;:&quot;Croacia Premijer Liga&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414635&quot;,&quot;t&quot;:&quot;J. Tichy - R. Merkl&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414846&quot;,&quot;t&quot;:&quot;Andrii Regush - V. Korobko&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414947&quot;,&quot;t&quot;:&quot;A. Sydorenko - H. Buianover&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414445&quot;,&quot;t&quot;:&quot;I. Todiras - I. Uzun&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414473&quot;,&quot;t&quot;:&quot;Jan Seeman - Filip Kubos&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30414485&quot;,&quot;t&quot;:&quot;S. Yureneva - O. Yureneva&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Femenina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412788&quot;,&quot;t&quot;:&quot;Wolves (lzrn) - Tottenham Hotspur (aguuero)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - FA Cup Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30413318&quot;,&quot;t&quot;:&quot;Brighton (Cofardi) - Leicester (Linox)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - FA Cup Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412233&quot;,&quot;t&quot;:&quot;Bayer 04 Leverkusen (Koss) - Borussia Dortmund (Fireball)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta Bundesliga Battle - 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412518&quot;,&quot;t&quot;:&quot;Eintracht Frankfurt (Sheva) - RB Leipzig (Profik)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta Bundesliga Battle - 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430419&quot;,&quot;t&quot;:&quot;Real Madrid (DIVINE) - Paris SG (FORCE)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430449&quot;,&quot;t&quot;:&quot;England (THREAT) - Spain (POWER)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430452&quot;,&quot;t&quot;:&quot;Arsenal (BLITZ) - Aston Villa (GRIMACE)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430783&quot;,&quot;t&quot;:&quot;Flamengo (Eliot) - Boca Juniors (Blake)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430742&quot;,&quot;t&quot;:&quot;Manchester City (Rose) - Spurs (Megan)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valkiria Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30412056&quot;,&quot;t&quot;:&quot;Houston Rockets (Pakapaka) - Phoenix Suns (Jovke)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - NBA Battle - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430658&quot;,&quot;t&quot;:&quot;Boston Celtics (Sparkz) - Oklahoma City Thunder (CHIEF)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430661&quot;,&quot;t&quot;:&quot;Miami Heat (CALAMITY) - Toronto Raptors (CRUCIAL)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30430756&quot;,&quot;t&quot;:&quot;Golden State Warriors (Tommy) - Brooklyn Nets (Donovan)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - Valhalla League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30413440&quot;,&quot;t&quot;:&quot;Winnipeg Jets (Wryi) - Dallas Stars (OneUniq)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ehockey - NHL Western Conference Battle - 3x4 mins&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30409757&quot;,&quot;t&quot;:&quot;M. Zakaria - T. Momen&quot;,&quot;ic&quot;:&quot;104&quot;,&quot;st&quot;:&quot;Open de Palm Hills Masculino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;es&quot;:null,&quot;t&quot;:null,&quot;l&quot;:[{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1747526412212071&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;27&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1747526414893670&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;28&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;ine&quot;:false,&quot;hml&quot;:true},&quot;subscription&quot;:{&quot;type&quot;:14,&quot;param&quot;:{&quot;sdd&quot;:[],&quot;ste&quot;:[1],&quot;spe&quot;:null,&quot;cc&quot;:&quot;ES&quot;,&quot;ec&quot;:[&quot;3 W\u0026B&quot;,&quot;6 W\u0026B&quot;]}},&quot;wid&quot;:&quot;w_1-p_4-wt_6&quot;,&quot;selectedEvent&quot;:{&quot;sec&quot;:&quot;pse&quot;,&quot;ty&quot;:2,&quot;c&quot;:&quot;30406729&quot;,&quot;t&quot;:&quot;E. Nava - B. Van De Zandschulp&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;Roland Garros Masculino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},&quot;hasVideoSelector&quot;:true,&quot;resources&quot;:{&quot;greyhounds&quot;:&quot;Galgos&quot;,&quot;horses&quot;:&quot;Caballos&quot;,&quot;greyhoundsAndHorses&quot;:&quot;Carreras 24 h&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;},&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>
                    <ul class="str__controls jstroplst">

                            <li data-t="4" class="str__control_item jstropt none">
                                <i class="ico-s icon-expand"></i>
                            </li>
                            <li data-t="5" class="str__control_item jstropt ">
                                <i class="ico-s icon-contract"></i>
                            </li>

                                <li data-t="1" class="str__control_item jstropt jpinunpin">
                                    <i class="ico-s icon-pin"></i>
                                </li>


                                <li data-t="6" class="str__control_item jstropt jminmag">
                                    <i class="ico-l icon-chevron-down"></i>
                                </li>
                    </ul>
                </div>
                <div class="play jplayerWrapper" data-pt="1">




    <div id="video" class="jintPlayer none" data-pt="1" data-pid="1" data-src="" data-prot="1" data-apiurl="https://api.livestreaming.imgarena.com/api/v2/streaming/events/486240/stream?operatorId=25&amp;auth=a72823005f4dc6cc60c319816b734860&amp;timestamp=1748196242775&amp;page.page=1&amp;page.size=1" data-apihead="null" data-an="UA-34961270-1" data-drm="">

    <script src="/js/video.js?v=cgtYl4qcGXYRWYqGwa16sWUVoL1Gml9DOfVHMaQMUJw"></script>
    <div id="videocontainer">
        <video class="jshakaplayer vjs-fluid" disableremoteplayback="" autoplay="" muted="muted">
        </video>
    </div>

    </div>

                    <p class="play_no_str__text jnovid none">
                        <span>
                            en este momento no hay video disponible
                        </span>
                    </p>
                </div>

                <a href="/live/e-nava-b-van-de-zandschulp-sc30406729" class="str__bets-link jlink" title="E. Nava - B. Van De Zandschulp">
                    Ver apuestas
                    <i class="ico-s icon__bold icon-chevron-thin-right"></i>
                </a>
        </div>
    </div>
    <div id="login" class="jstPrEnded widget__login_bg none">

        <div class="widget__login">
            <a class="btn btn-m btn__contrast-outline jlb jt_streamingLog">
                Entrar a mi cuenta
            </a>
            <span class="widget__login_footer-links">
                <a class="widget__login_text_button jlink jt_streamingReg">
                    Quiero registrarme
                    <i class="icon-text-arrow-right icon__bold"></i>
                </a>
            </span>
        </div>
    </div>
    <div data-jsfile="streaming.section.js?v=K9IXm3CDCeY7V2LPCt0n_uqSLa0Rayyp5b57q8Lt-Xk" class="ljs" hidden="hidden"></div>

    </div>
    <div data-jsfile="streaming.widget.js?v=y6DsDbtcBFroCKpeEqKty8uFmvFPmuNsaRhIDA1X26c" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw4-1" data-v="{&quot;QueryStringEventId&quot;:0,&quot;IsPinUnpinEnabled&quot;:true,&quot;HasMinimizeMagnifyOption&quot;:true,&quot;IsOnlyActiveInUnpinnedMode&quot;:true,&quot;HasVideoSelector&quot;:true,&quot;HasScrollTopButton&quot;:false,&quot;DoesShowBetsLinkBar&quot;:true,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_2-p_4-wt_106_c" class="jqw  widget_type_106_c" data-wt="106" data-pa="4" data-co="0" data-po="2" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="70" data-nrc="0" data-ic="true" data-vtw="null" data-sn="BetslipUserBetsSwitcher">




    <div class="jdata" data-section="betslipUserBetsSwitcher" data-hash="BbkDGL4-jAGQsuevbrrZIAnz05UnQRKYzMPZaF4Usuw"></div>

    <nav class="ticket__nav jbusw
        jcol collapsed
        ">
        <div hidden="" class="jdata" data-btype="106" data-bsec="Betslip" data-utype="106" data-usec="UserBets" data-csu="true" data-ssec="Betslip"></div>
        <div class="ticket__nav-item">
            <div class="switcher-content switcher-content--ticket">
                <input id="rbet" type="radio" value="betslip" name="switcher">
                <label for="rbet">
                    Boleto
                    <span class="jqlop counter counter--small">
                        0
                    </span>
                </label>
                <input id="ruserb" type="radio" value="userbets" name="switcher">
                <label for="ruserb">
                    Mis apuestas
                </label>
            </div>
        </div>
            <i class="jbback ticket__nav-item icon-chevron-thin-down ico-s jt_bcDesplegar"></i>
    </nav>
    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw4-2" data-v="{&quot;ShowBack&quot;:true,&quot;IsUserBetsAlwaysEnabled&quot;:true,&quot;ParentHtmlId&quot;:&quot;w_2-p_4-wt_106_c&quot;,&quot;HtmlId&quot;:&quot;w_2-p_4-wt_106_c_BetslipUserBetsSwitcher&quot;,&quot;ClassName&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_3-p_4-wt_106_c" class="jqw  none  betslip_container janimateSquare widget_type_106_c" data-wt="106" data-pa="4" data-co="0" data-po="3" data-sw="false" data-vi="False" data-sl="True" data-ti="False" data-sc="False" data-pwi="47" data-nrc="0" data-ic="true" data-vtw="null" data-sn="Betslip">




    <div class="jdata" data-section="betslip" data-hash="vnV6cqKXy3pWeR7VcxlQgtaUIJjHfQl5D-aHsjjOQMY"></div>

<article class="ticket animated jstep" data-step="0">
    <div class="ticket__content ticket__content--empty wrapper-large">
        <div class="ticket__titulo">
            <div class="ticket__illustration">
                <i class="icon-ticket"></i>
            </div>
            <h6 class="title title_l">
                El boleto está vacio
            </h6>
        </div>
        <div class="ticket__texto text">
            <p class="title title_m">
                ¡No hay apuestas seleccionadas!
            </p>
            <p>
                Por favor, navega por nuestra oferta deportiva y selecciona tus apuestas
            </p>
        </div>
        <ul class="list-nav">
            <li>
                <a href="/live" data-url="/live" class="jemptyp list-nav__item jt_bcIr" data-lnk="Live">
                    <i class="ico-m icon-live list-nav__icon"></i>
                    <span class="list-nav__texto text">
                        Live
                    </span>
                    <span class="list-nav__numero">148</span>
                    <i class="ico-s icon-chevron-thin-right list-nav__arrow"></i>
                </a>
            </li>
            <li>
                <a href="/calendario" data-url="/calendario" class="jemptyp list-nav__item jt_bcIr" data-lnk="Calendario">
                    <i class="ico-m icon-calendar list-nav__icon"></i>
                    <span class="list-nav__texto text">
                        Hoy
                    </span>
                    <span class="list-nav__numero">1299</span>
                    <i class="ico-s icon-chevron-thin-right list-nav__arrow"></i>
                </a>
            </li>
            <li>
                <a href="/" data-url="/" class="jemptyp list-nav__item jt_bcIr" data-lnk="Home">
                    <i class="ico-m icon-home list-nav__icon"></i>
                    <span class="list-nav__texto text">
                        Inicio
                    </span>
                    <i class="ico-s icon-chevron-thin-right list-nav__arrow"></i>
                </a>
            </li>
        </ul>
    </div>
</article><div class="jbsloading loading ticket__panel none">
    <div class="windows8">
    <div class="wBall" id="wBall_1">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_2">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_3">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_4">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_5">
        <div class="wInnerBall"></div>
    </div>
    <i class="icon-reta2"></i>
</div>
</div>    <div data-jsfile="betslip.section.js?v=vnV6cqKXy3pWeR7VcxlQgtaUIJjHfQl5D-aHsjjOQMY" class="ljs" hidden="hidden"></div>
    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw4-3" data-v="{&quot;ParentHtmlId&quot;:&quot;w_3-p_4-wt_106_c&quot;,&quot;HtmlId&quot;:&quot;w_3-p_4-wt_106_c_Betslip&quot;,&quot;ClassName&quot;:&quot;betslip_container janimateSquare&quot;,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_14-p_4-wt_106_c" class="jqw  none  betslip_container betslip_container--userbets widget_type_106_c" data-wt="106" data-pa="4" data-co="0" data-po="14" data-sw="false" data-vi="False" data-sl="True" data-ti="False" data-sc="False" data-pwi="95" data-nrc="0" data-ic="true" data-vtw="null" data-sn="UserBets">




    <div class="jdata" data-section="userBets" data-hash="hKDWbB_fFs9EpiXVJ9ma-jw8hruY6b58T-m1AOQgIa4"></div>


<div class="ticket__content ticket__content--loggedout wrapper-large jlogin">
    <div class="ticket__titulo">
        <div class="ticket__illustration">
            <i class="icon-user-ticket"></i>
        </div>
        <h6 class="title title_m title--minus">
            Para ver tus apuestas:
        </h6>
    </div>
    <div class="ticket__texto">
        <button class="btn btn-m btn__secondary-outline jlog">
            Entra en tu cuenta
        </button>
        <p>
            o <a href="/registro" class="jlink"><span class="link-inline">regístrate</span> <i class="icon-text-arrow-right"></i></a>
        </p>
    </div>
</div>

<div data-jsfile="userBets.section.js?v=hKDWbB_fFs9EpiXVJ9ma-jw8hruY6b58T-m1AOQgIa4" class="ljs" hidden="hidden"></div>    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw4-14" data-v="{&quot;DateFrom&quot;:&quot;2025-05-22T00:00:00&quot;,&quot;DateTo&quot;:&quot;2025-05-25T23:59:59&quot;,&quot;LastDays&quot;:0,&quot;StatusConfigurations&quot;:[{&quot;Status&quot;:3,&quot;ShowDateFilter&quot;:false,&quot;LastDays&quot;:null,&quot;IconClass&quot;:null},{&quot;Status&quot;:2,&quot;ShowDateFilter&quot;:false,&quot;LastDays&quot;:null,&quot;IconClass&quot;:null},{&quot;Status&quot;:4,&quot;ShowDateFilter&quot;:false,&quot;LastDays&quot;:30,&quot;IconClass&quot;:null},{&quot;Status&quot;:1,&quot;ShowDateFilter&quot;:true,&quot;LastDays&quot;:null,&quot;IconClass&quot;:&quot;ico-m icon-calendar&quot;}],&quot;Status&quot;:null,&quot;TabsClasses&quot;:null,&quot;ContainerClasses&quot;:&quot;ticket__userbets&quot;,&quot;TabsNavClasses&quot;:&quot;tab__group--fullwidth&quot;,&quot;AlwaysVisible&quot;:false,&quot;ShowNotLoggedInView&quot;:false,&quot;ZIndex&quot;:0,&quot;ParentHtmlId&quot;:null,&quot;HtmlId&quot;:null,&quot;ClassName&quot;:&quot;betslip_container betslip_container--userbets&quot;,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
    <section data-cont="6" class="jpanel searcher__panel">


    <section id="w_1-p_6-wt_106_c" class="jqw  widget_type_106_c" data-wt="106" data-pa="6" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="24" data-nrc="0" data-ic="true" data-vtw="null" data-sn="Searcher">




    <div class="jdata" data-section="searcher" data-hash="u_iuzCffABACpNOUqQuIv5nH1YJEH72wMOFJqu5etGU"></div>
<div class="jsearcherpanel">

</div>

<div data-jsfile="searcher.section.js?v=u_iuzCffABACpNOUqQuIv5nH1YJEH72wMOFJqu5etGU" class="ljs" hidden="hidden"></div>    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw6-1" data-v="{&quot;MaxPromotedElements&quot;:15,&quot;MaxSuggestElements&quot;:10,&quot;MaxResultElements&quot;:15,&quot;InputText&quot;:null,&quot;IsSearch&quot;:false,&quot;ParentHtmlId&quot;:&quot;w_1-p_6-wt_106_c&quot;,&quot;HtmlId&quot;:&quot;w_1-p_6-wt_106_c_Searcher&quot;,&quot;ClassName&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
</div>
    </div>
    <div class="alay"></div>
</main>
</div>

    <div id="pamc">
        <div class="modal jmo " style="display:none;">
    <div class="modal__wrapper">
        <form class="modal__content animate" action="/deportes/futbol/segunda-division/2" method="post">
            <div class="modal__header">
    <h4 id="modalHeader">
    </h4>
        <span class="jmocl close"><i class="icon-multiply"></i></span>
</div>
<div id="modalBody" class="modal__body">
</div>
        </form>
    </div>
</div>
    </div>

<script defer="" src="https://www.retabet.es/js/cookiemodal.js"></script>
<div class="jpckmsg" data-ckdom="1" data-cui="es-ES" hidden=""></div>
<div data-jsfile="cookieConfigMessage.section.js?v=vJzT3Wcgi-w6A4cyOBQsaqApYiX6nfMUPDbLtpfk7Tg" class="ljs" hidden="hidden"></div>

    <div>
    <div class="modal jmo modal_session" id="sessionCountdownMessage" style="display:none;">
    <div class="modal__wrapper">
        <form class="modal__content animate" action="/deportes/futbol/segunda-division/2" method="post">
            <div class="modal__header">
    <h4 id="modalHeader">
Tu sesión online esta apunto de caducar    </h4>
        <span class="jmocl close"><i class="icon-multiply"></i></span>
</div>
<div id="modalBody" class="modal__body">
<div class="modal__title">
    <h4>Tu sesión online caducará en breve</h4>
</div>
<div class="modal__container">
    <div class="modal__box">
        <div class="jtmpl" hidden="">{sec}s.</div>
        <span class="modal__num jval"></span>
        <p>
             Porfavor haz click en "Continuar" para seguir jugando o haz click en "Salir" para terminar ahora tu sesión
        </p>
    </div>
</div>
<div class="modal__footer">
    <div class="botonera">
        <button type="button" class="jcontinue btn btn-m btn__secondary-outline">
            <span>Continuar</span>
        </button>
        <button type="button" class="jlogOff btn btn-m btn__secondary-outline">
            <span>Salir</span>
        </button>
    </div>
</div>
</div>
        </form>
    </div>
</div>
</div>


<div id="casinoMessage">
    <div class="modal jmo " style="display:none;">
    <div class="modal__wrapper">
        <form class="modal__content animate" action="/deportes/futbol/segunda-division/2" method="post">
            <div class="modal__header">
    <h4 id="modalHeader">
    </h4>
</div>
<div id="modalBody" class="modal__body">
</div>
        </form>
    </div>
</div>
</div>

<div data-jsfile="casinoMessage.section.js?v=i5QENHiJ4mx5hJwYbRxUCOoX2q05PcIXDfGpWKa3jn0" class="ljs" hidden="hidden"></div>


    <footer class="jfooter ">
<section class="footer__cont">
  <nav class="footer__nav">
    <div class="footer__menu">
      <h3>
        <a href="/" title="Deportes">Deportes</a>
      </h3>
      <ul>
        <li class="footer__menu-item">
          <a href="/" title="Apuestas deportivas">Apuestas deportivas</a>
        </li>
        <li class="footer__menu-item">
          <a href="/live" title="Apuestas en directo">Apuestas en directo</a>
        </li>
        <li class="footer__menu-item">
          <a href="/deportes/futbol-m1" title="Apuestas de fútbol">Apuestas de fútbol</a>
        </li>
        <li class="footer__menu-item">
          <a href="/deportes/baloncesto-m5" title="Apuestas de baloncesto">Apuestas de baloncesto</a>
        </li>
        <li class="footer__menu-item">
          <a href="/deportes/tenis-m8" title="Apuestas de tenis">Apuestas de tenis</a>
        </li>
        <li class="footer__menu-item">
          <a href="/deportes/esports" title="Apuestas de Esports">Apuestas de Esports</a>
        </li>
        <li class="footer__menu-item">
          <a href="/juegos-virtuales" title="Apuestas virtuales">Apuestas virtuales</a>
        </li>
      </ul>
    </div>
    <div class="footer__menu">
      <h3>
        <a href="/casino" title="Casino">Casino</a>
      </h3>
      <ul>
        <li class="footer__menu-item">
          <a href="/casino" title="Juegos de casino">Juegos de casino</a>
        </li>
        <li class="footer__menu-item">
          <a href="/ruleta-en-vivo" title="Ruleta en vivo">Ruleta en vivo</a>
        </li>
        <li class="footer__menu-item">
          <a href="/slots" title="Slots online">Slots online</a>
        </li>
        <li class="footer__menu-item">
          <a href="/blackjack" title="Blackjack online">Blackjack online</a>
        </li>
      </ul>
    </div>
    <div class="footer__menu">
      <h3>
        <a href="https://www.retabet.es/?setUG=true#aboutSec" target="_blank" title="Sobre nosotros">Sobre nosotros</a>
      </h3>
      <ul>
        <li class="footer__menu-item">
          <a href="https://www.retabet.es/?setUG=true&amp;map&amp;utm_source=Mailify&amp;utm_medium=email&amp;utm_campaign=((News))#establishmentsSec" target="_blank" title="Tiendas y locales">Tiendas y locales</a>
        </li>
        <li class="footer__menu-item">
          <a href="https://retabet.es/mobile" target="_blank" title="Descargar Apps">Descargar Apps</a>
        </li>
        <li class="footer__menu-item">
          <a href="https://blog.retabet.es/" target="_blank" title="Blog">Blog</a>
        </li>
        <li class="footer__menu-item">
          <a href="/contacto#afiliados" title="Afiliados">Afiliados</a>
        </li>
        <li class="footer__menu-item">
          <a href="/contacto" title="Contacto">Contacto</a>
        </li>
        <li class="footer__menu-item">
          <a href="https://www.retabet.es/files/es/pdf/Clausula_informativa_tratamiento_ESTATAL.pdf" title="Cláusulas informativas" target="_blank">Cláusulas informativas</a>
        </li>
        <li class="footer__menu-item">
          <a href="https://www.retabet.es/files/es/pdf/normativa_RETA_Estatal.pdf" title="Normativa Retabet" target="_blank">Normativa Retabet</a>
        </li>
        <li class="footer__menu-item">
          <a href="/sitemap" title="Mapa del sitio">Mapa del sitio</a>
        </li>
      </ul>
    </div>
    <div class="footer__menu">
      <h3>
        <a href="/ayuda" title="Sobre nosotros">Ayuda</a>
      </h3>
      <ul>
        <li class="footer__menu-item">
          <a href="/ayuda#tarjeta_reta" title="Tarjeta Retabet">Tarjeta Retabet</a>
        </li>
        <li class="footer__menu-item">
          <a href="/ayuda#metodos_ingreso" title="Métodos de ingreso">Métodos de ingreso</a>
        </li>
        <li class="footer__menu-item">
          <a href="/ayuda#metodos_cobro" title="Métodos de cobro">Métodos de cobro</a>
        </li>
        <li class="footer__menu-item">
          <a href="/ayuda#normativa_retabet" title="Reglas de juego">Reglas de juego</a>
        </li>
      </ul>
    </div>
    <div class="footer__menu">
      <h3>
        <a href="/juego-mas-seguro" title="Juego más seguro">Juego más seguro</a>
      </h3>
      <ul>
        <li class="footer__menu-item">
          <a href="/juego-mas-seguro" title="Medidas multidisciplinares">Medidas multidisciplinares</a>
        </li>
        <li class="footer__menu-item">
          <a href="/juego-mas-seguro" title="¿Tengo problemas con el juego?">¿Tengo problemas con el juego?</a>
        </li>
        <li class="footer__menu-item">
          <a href="/autoexclusion" title="Autoexclusión">Autoexclusión</a>
        </li>
      </ul>
    </div>
    <div class="footer__menu">
      <h3>
        <a href="/juego-autorizado" title="Juego autorizado">Juego autorizado</a>
      </h3>
      <ul>
        <li class="footer__menu-item">
          <a href="/juego-autorizado" title="juego autorizado">Juego autorizado</a>
        </li>
      </ul>
    </div>
  </nav>
  <div class="footer__icons">
    <ul class="footer__payment">
      <li>
        <i class="icon-tarjeta-reta"></i>
      </li>
      <li>
        <i class="logos-cc-visa"></i>
      </li>
      <li>
        <i class="logos-mastercard"></i>
      </li>
      <li>
        <i class="logos-cc-paypal"></i>
      </li>
      <li>
        <i class="icon-tienda"></i>
      </li>
      <li>
        <i class="logos-bizum2"></i>
      </li>
    </ul>
    <ul class="footer__logos footer__logos--estatal">
      <li class="footer__logo footer__logo--diversion">
        <a href="https://www.ordenacionjuego.es/operadores-juego/operadores-licencia/operadores/ekasa-apuestas-online-sa" title="sin diversión no hay juego">
          <img src="https://cdn.retabet.es/apuestas/es/webfooterimages/sindiversion_nojuego.svg" alt="sin diversión no hay juego" loading="lazy">
        </a>
      </li>
      <li class="footer__logo footer__logo--responsable">
        <a href="https://www.ordenacionjuego.es/operadores-juego/operadores-licencia/operadores/ekasa-apuestas-online-sa" title="juega responsable">
          <img src="https://cdn.retabet.es/apuestas/es/webfooterimages/juega_responsable.svg" alt="juega responsable" loading="lazy">
        </a>
      </li>
      <li class="footer__logo">
        <a href="https://www.ordenacionjuego.es/participantes-juego/juego-seguro/rgiaj" title="autoprohibicion">
          <img src="https://cdn.retabet.es/apuestas/es/webfooterimages/autoprohibicion.svg" alt="autoprohibicion" loading="lazy">
        </a>
      </li>
      <li class="footer__logo">
        <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2011-9280 " title="mas18">
          <img src="https://cdn.retabet.es/apuestas/es/webfooterimages/mas_18.svg" alt="mas18" loading="lazy">
        </a>
      </li>
      <li class="footer__logo footer__logo--bien">
        <a href="https://www.ordenacionjuego.es/participantes-juego/juego-autorizado" title="Juego autorizado">
          <img src="https://cdn.retabet.es/apuestas/es/webfooterimages/logo-juego-autorizado.jpg" alt="Juego autorizado" loading="lazy">
        </a>
      </li>
      <li class="footer__logo footer__logo--seguro">
        <a href="https://www.ordenacionjuego.es/participantes-juego/juego-seguro" title="jugar seguro">
          <img src="https://cdn.retabet.es/apuestas/es/webfooterimages/juego_seguro.png" alt="Juego seguro" loading="lazy">
        </a>
      </li>
    </ul>
  </div>
</section>
<section class="footer__business-info">
  <div>
    <p class="footer__text"> © EKASA apuestas online S.A., Parque Tecnológico de Zamudio edificio. 407 1ª planta, 48170 ZAMUDIO (BIZKAIA) · A95774857 · Licencias concedidas por la DGOJ 326/GA/1060, 327/GO/1060, 341/ADC/1060, 340/AOC/1060, 451/AHC/1060, 454/MAZ/1060, 455/BLJ/1060 y 456/RLT/1060.
    </p>
    <ul class="footer__social">
      <li>
        <a href="https://www.facebook.com/Retabet" target="_blank" title="Facebok">
          <i class="icon-facebook"></i>
        </a>
      </li>
      <li>
        <a href="https://twitter.com/Retabet?lang=es" target="_blank" title="Twitter">
          <i class="icon-logoX"></i>
        </a>
      </li>
      <li>
        <a href="https://www.instagram.com/retabet/" target="_blank" title="Instagram">
          <i class="icon-instagram"></i>
        </a>
      </li>
    </ul>
  </div>
  <div>
    <ul class="footer__links">
      <li>
        <a href="https://www.retabet.es/files/es/pdf/politica-privacidad-Grupo-Retabet.pdf" target="_blank" title="Política de privacidad">Política de privacidad</a>
      </li>
      <li>
        <a href="https://www.retabet.es/files/es/pdf/contrato-de-juego-Retabet-Apuestas.pdf" target="_blank" title="Términos y condiciones">Términos y condiciones</a>
      </li>
      <li>
        <a href="/politica-cookies" title="Política de cookies" target="_blank">Política de cookies</a>
      </li>
    </ul>
  </div>
</section>        <div hidden="" id="initHora" data-hour="20" data-min="4" data-sec="2"></div>
        <section class="footer__time">
            <div class="footer__time-box">
                <span id="hora"></span>

    <div tabindex="0" class="select-noform select-noform-dark jdivtz ">
        <div class="select-noform_active">
            <span>(UTC+01:00) Bruselas, Copenhague, Madrid, París</span>
        </div>
        <ul id="tzlst" class="none select-noform__options ps_scroll"></ul>
    </div>

            </div>
            <div class="footer__lastlogin">



            </div>
        </section>
    <div class="modal jmo " style="display:none;">
    <div class="modal__wrapper">
        <form class="modal__content animate" action="/deportes/futbol/segunda-division/2" method="post">
            <div class="modal__header">
    <h4 id="modalHeader">
    </h4>
        <span class="jmocl close"><i class="icon-multiply"></i></span>
</div>
<div id="modalBody" class="modal__body">
</div>
        </form>
    </div>
</div>
</footer>

<div data-jsfile="footer.section.js?v=5czERWbmkzVlFPzd-dkWtxxyIaPG-f9BY6lDUNjSa4Q" class="ljs" hidden="hidden"></div>



<div id="msgList">
</div>

<div id="amtp" hidden="hidden">

    <div class="jm jmsg msg msg-generic msg--error animated fadeInDown none" data-tp="6" data-ocl="true">
            <span class="msg__icon icon__bold"></span>
<div class="msg__text_content">
        <p class="msg__title title_m jmti">
        </p>
        <p class="msg__text jmtx">
        </p>
</div>            <span class="jmcls msg__close icon__bold ico-s" onclick="$(this).parent().remove();"></span>

    </div>

    <div class="jm jmsg msg msg-generic msg--success animated fadeInDown none" data-tp="5" data-ocl="true">
            <span class="msg__icon icon__bold"></span>
<div class="msg__text_content">
        <p class="msg__title title_m jmti">
        </p>
        <p class="msg__text jmtx">
        </p>
</div>            <span class="jmcls msg__close icon__bold ico-s" onclick="$(this).parent().remove();"></span>

    </div>

    <div class="jm jmsg msg msg-generic msg--warning animated fadeInDown none" data-tp="7" data-ocl="true">
            <span class="msg__icon icon__bold"></span>
<div class="msg__text_content">
        <p class="msg__title title_m jmti">
        </p>
        <p class="msg__text jmtx">
        </p>
</div>            <span class="jmcls msg__close icon__bold ico-s" onclick="$(this).parent().remove();"></span>

    </div>

    <div class="jm jmsg msg msg-generic msg--info animated fadeInDown none" data-tp="8" data-ocl="true">
            <span class="msg__icon icon__bold"></span>
<div class="msg__text_content">
        <p class="msg__title title_m jmti">
        </p>
        <p class="msg__text jmtx">
        </p>
</div>            <span class="jmcls msg__close icon__bold ico-s" onclick="$(this).parent().remove();"></span>

    </div>
</div>

<div id="amst" hidden="hidden">
    <span class="amstm" data-id="1">Sin conexión</span>
    <span class="amstm" data-id="2">Debes iniciar sesión para ver esta sección</span>
    <span class="amstm" data-id="3">Error al intentar abrir el juego, intentalo mas tarde</span>
    <span class="amstm" data-id="5">El usuario está autoexcluido en casino y no puede jugar.</span>
    <span class="amstm" data-id="6">El usuario está autoexcluido en casino y no puede jugar</span>
    <span class="amstm" data-id="7">El usuario está autoexcluido en slots y no puede jugar</span>
    <span class="amstm" data-id="8">Lo sentimos ha ocurrido un error, <b>cierra el navegador y vuelve a intentarlo más tarde</b>. Si el problema persiste, contacta con nuestro Servicio de Atención al Cliente. Referencia: {error}</span>
</div>
    <div class="jsiteloading loading" style="display: none;">
    <div class="windows8">
    <div class="wBall" id="wBall_1">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_2">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_3">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_4">
        <div class="wInnerBall"></div>
    </div>
    <div class="wBall" id="wBall_5">
        <div class="wInnerBall"></div>
    </div>
    <i class="icon-reta2"></i>
</div>
</div>




    <div id="w-chbot" class="jcd" data-providerid="1" data-startonopen="true" data-is="true" data-io="false" data-chs="0">

    <div hidden="" class="jxc" data-key="def3dc47-abc2-4288-8ced-ac937b544c66" data-cau="False" data-cid="0" data-cia="False" data-cug="apuestas" data-cde="0" data-ccd="retabet.es" data-utzs="1" data-ugtzs="1">
    </div>
    </div>

<div data-jsfile="chatBot2.section.js?v=QlOZAKyf6jJVmYDuEjxNwDf-hMlbpXdtsZWB2F4LLPI" class="ljs" hidden="hidden"></div>
    <img class="reta-square" src="/reta-square.jpg?638837930428071175" alt="Retabet square" style="max-width:0%">




    <div id="modalFactory">

        <div class="modal jmo jModal" style="display:none;">
            <div class="modal__wrapper">
                    <form class="modal__content animate jcontent jformModal" action="/deportes/futbol/segunda-division/2" method="post">

        <div class="modal__header jheader">
            <h4 id="modalHeader">
            </h4>
                <span class="jmocl close"><i class="icon-multiply"></i></span>
        </div>
        <div id="modalBody" class="modal__body">
        </div>

                    </form>
            </div>
        </div>

    </div>


<iframe name="TS_Injection" style="width: 0px; height: 0px; visibility: hidden; display: none;"></iframe></body></html>
"""
from parsel import Selector
import re
import dateparser
import json
import ast
import datetime
import traceback
import pytz
# from bookies_configurations import list_of_markets_V2

html_cleaner = re.compile("<.*?>")

response = Selector(response)
match_infos = []
# list_of_markets = list_of_markets_V2["Luckia"]["1"]
# print("list_of_markets", list_of_markets)

# xpath_results = response.xpath(
#                 "//li[contains(@class, 'com-coupon-line-new-layout betbutton-layout avb-row avb-table market-avb')]").extract()
try:
    xpath_results = response.xpath("//li[@class='jlink jev event__item']").extract()
    match_infos = []
    for xpath_result in xpath_results:
        try:
            xpath_result = Selector(xpath_result)
            home_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[0]
            away_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[1]
            url = xpath_result.xpath("//li[@class='jlink jev event__item']/@data-u").extract()[0]
            url = "https://apuestas.retabet.es" + url
            web_url = url
            date = xpath_result.xpath("//span[@class='event__day']/text()").extract()[0]
            time = xpath_result.xpath("//span[@class='event__time']/text()").extract()[0]
            date = dateparser.parse(''.join(date + " " + time))
            if "/live/" not in url:
                print(url, web_url, home_team, away_team, date)

        except Exception as e:
            continue
except Exception as e:
    print(traceback.format_exc())
print(match_infos)
