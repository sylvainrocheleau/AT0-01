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
window.gACM=!!window.gACM;try{(function(){(function(){var l={decrypt:function(l){try{return JSON.parse(function(l){l=l.split("l");var O="";for(var Z=0;Z<l.length;++Z)O+=String.fromCharCode(l[Z]);return O}(l))}catch(Z){}}};return l={configuration:l.decrypt("123l34l97l99l116l105l118l101l34l58l34l110l111l34l44l34l100l101l98l117l103l103l105l110l103l34l58l34l110l111l34l44l34l109l111l100l117l108l101l49l34l58l34l101l110l97l98l108l101l100l34l44l34l109l111l100l117l108l101l50l34l58l34l101l110l97l98l108l101l100l34l44l34l109l111l100l117l108l101l51l34l58l34l101l110l97l98l108l101l100l34l44l34l109l111l100l117l108l101l52l34l58l34l101l110l97l98l108l101l100l34l125")}})();
var ol=77;try{var zl,sl,_l=L(491)?0:1,Il=L(566)?0:1,lL=L(444)?0:1,OL=L(836)?0:1,zL=L(409)?0:1,iL=L(65)?1:0,IL=L(431)?0:1;for(var jL=(L(808),0);jL<sl;++jL)_l+=L(983)?1:2,Il+=(L(912),2),lL+=(L(65),2),OL+=(L(999),2),zL+=L(384)?2:1,iL+=L(36)?2:1,IL+=(L(905),3);zl=_l+Il+lL+OL+zL+iL+IL;window.Zz===zl&&(window.Zz=++zl)}catch(lo){window.Zz=zl}var Lo=!0;function z(l,O){l+=O;return l.toString(36)}
function Oo(l){var O=91;!l||document[s(O,209,196,206,196,189,196,199,196,207,212,174,207,188,207,192)]&&document[S(O,209,196,206,196,189,196,199,196,207,212,174,207,188,207,192)]!==S(O,209,196,206,196,189,199,192)||(Lo=!1);return Lo}function S(l){var O=arguments.length,Z=[];for(var _=1;_<O;++_)Z.push(arguments[_]-l);return String.fromCharCode.apply(String,Z)}function Zo(){}Oo(window[Zo[z(1086777,ol)]]===Zo);Oo(typeof ie9rgb4!==S(ol,179,194,187,176,193,182,188,187));
Oo(RegExp("\x3c")[s(ol,193,178,192,193)](function(){return"\x3c"})&!RegExp(z(42812,ol))[z(1372128,ol)](function(){return"'x3'+'d';"}));
var so=window[S(ol,174,193,193,174,176,181,146,195,178,187,193)]||RegExp(s(ol,186,188,175,182,201,174,187,177,191,188,182,177),S(ol,182))[z(1372128,ol)](window["\x6e\x61vi\x67a\x74\x6f\x72"]["\x75\x73e\x72A\x67\x65\x6et"]),_o=+new Date+(L(360)?6E5:746209),io,Jo,lO,LO=window[s(ol,192,178,193,161,182,186,178,188,194,193)],zO=so?L(233)?3E4:19714:L(669)?7606:6E3;
document[S(ol,174,177,177,146,195,178,187,193,153,182,192,193,178,187,178,191)]&&document[S(ol,174,177,177,146,195,178,187,193,153,182,192,193,178,187,178,191)](s(ol,195,182,192,182,175,182,185,182,193,198,176,181,174,187,180,178),function(l){var O=11;document[S(O,129,116,126,116,109,116,119,116,127,132,94,127,108,127,112)]&&(document[S(O,129,116,126,116,109,116,119,116,127,132,94,127,108,127,112)]===s(O,115,116,111,111,112,121)&&l[S(O,116,126,95,125,128,126,127,112,111)]?lO=!0:document[S(O,129,116,
126,116,109,116,119,116,127,132,94,127,108,127,112)]===z(68616527655,O)&&(io=+new Date,lO=!1,ZO()))});function ZO(){if(!document[s(91,204,208,192,205,212,174,192,199,192,190,207,202,205)])return!0;var l=+new Date;if(l>_o&&(L(106)?6E5:370616)>l-io)return Oo(!1);var O=Oo(Jo&&!lO&&io+zO<l);io=l;Jo||(Jo=!0,LO(function(){Jo=!1},L(483)?0:1));return O}ZO();var sO=[L(856)?26477630:17795081,L(914)?2147483647:27611931586,L(851)?951379742:1558153217];
function SO(l){var O=59;l=typeof l===z(1743045617,O)?l:l[s(O,175,170,142,175,173,164,169,162)](L(254)?36:49);var Z=window[l];if(!Z||!Z[S(O,175,170,142,175,173,164,169,162)])return;var _=""+Z;window[l]=function(l,O){Jo=!1;return Z(l,O)};window[l][S(O,175,170,142,175,173,164,169,162)]=function(){return _}}for(var iO=(L(534),0);iO<sO[z(1294399128,ol)];++iO)SO(sO[iO]);Oo(!1!==window[S(ol,180,142,144,154)]);window._O=window._O||{};window._O.Li="08254aa74d194000cd6f18c4b95d1560b8a5bc6e5183b80473d29ac746a77c0b5e80d0c1b6f2d7abd43a86736117af43a18c5f67295769c2a7c923ed22fab60a134bd6134d026c0b";
function jO(l){var O=+new Date,Z;!document[S(43,156,160,144,157,164,126,144,151,144,142,159,154,157,108,151,151)]||O>_o&&(L(979)?639190:6E5)>O-io?Z=Oo(!1):(Z=Oo(Jo&&!lO&&io+zO<O),io=O,Jo||(Jo=!0,LO(function(){Jo=!1},L(653)?0:1)));return!(arguments[l]^Z)}function s(l){var O=arguments.length,Z=[],_=1;while(_<O)Z[_-1]=arguments[_++]-l;return String.fromCharCode.apply(String,Z)}function L(l){return 389>l}
(function lz(O){O&&"number"!==typeof O||("number"!==typeof O&&(O=1E3),O=Math.max(O,1),setInterval(function(){lz(O-10)},O))})(!0);})();}catch(x){}finally{ie9rgb4=void(0);};function ie9rgb4(a,b){return a>>b>>0};

})();

</script>

<script type="text/javascript" src="/TSPD/082eaff409ab2000c75e911f854dd124762af04064d3c351d6eac7c588b20793170a288b0c11632d?type=9"></script>

<script type="text/javascript">
(function(){
window.gACM=!!window.gACM;try{(function(){(function oz(){var O=!1;function Z(O){for(var Z=0;O--;)Z+=_(document.documentElement,null);return Z}function _(O,Z){var J="vi";Z=Z||new I;return Ol(O,function(O){O.setAttribute("data-"+J,Z.i1());return _(O,Z)},null)}function I(){this.Zi=1;this.i_=0;this.sz=this.Zi;this.Os=null;this.i1=function(){this.Os=this.i_+this.sz;if(!isFinite(this.Os))return this.reset(),this.i1();this.i_=this.sz;this.sz=this.Os;this.Os=null;return this.sz};this.reset=function(){this.Zi++;this.i_=0;this.sz=this.Zi}}var J=!1;
function ll(O,Z){var _=document.createElement(O);Z=Z||document.body;Z.appendChild(_);_&&_.style&&(_.style.display="none")}function Ll(Z,_){_=_||Z;var I="|";function ll(O){O=O.split(I);var Z=[];for(var _=0;_<O.length;++_){var J="",Ll=O[_].split(",");for(var Ol=0;Ol<Ll.length;++Ol)J+=Ll[Ol][Ol];Z.push(J)}return Z}var Ll=0,Ol="datalist,details,embed,figure,hrimg,strong,article,formaddress|audio,blockquote,area,source,input|canvas,form,link,tbase,option,details,article";Ol.split(I);Ol=ll(Ol);Ol=new RegExp(Ol.join(I),
"g");while(Ol.exec(Z))Ol=new RegExp((""+new Date)[8],"g"),O&&(J=!0),++Ll;return _(Ll&&1)}function Ol(O,Z,_){(_=_||J)&&ll("div",O);O=O.children;var I=0;for(var Ll in O){_=O[Ll];try{_ instanceof HTMLElement&&(Z(_),++I)}catch(Ol){}}return I}Ll(oz,Z)})();var ol=77;
try{var zl,sl,_l=L(687)?0:1,Il=L(759)?0:1,lL=L(272)?1:0,OL=L(942)?0:1,zL=L(729)?0:1,iL=L(512)?0:1,IL=L(397)?0:1;for(var jL=(L(510),0);jL<sl;++jL)_l+=(L(118),2),Il+=(L(619),2),lL+=(L(531),2),OL+=(L(97),2),zL+=(L(72),2),iL+=L(539)?1:2,IL+=L(449)?1:3;zl=_l+Il+lL+OL+zL+iL+IL;window.Zz===zl&&(window.Zz=++zl)}catch(lo){window.Zz=zl}var Lo=!0;function s(l){var O=arguments.length,Z=[],_=1;while(_<O)Z[_-1]=arguments[_++]-l;return String.fromCharCode.apply(String,Z)}
function Oo(l){var O=19;!l||document[s(O,137,124,134,124,117,124,127,124,135,140,102,135,116,135,120)]&&document[s(O,137,124,134,124,117,124,127,124,135,140,102,135,116,135,120)]!==z(68616527647,O)||(Lo=!1);return Lo}function z(l,O){l+=O;return l.toString(36)}function Zo(){}Oo(window[Zo[z(1086777,ol)]]===Zo);Oo(typeof ie9rgb4!==z(1242178186122,ol));Oo(RegExp("\x3c")[z(1372128,ol)](function(){return"\x3c"})&!RegExp(s(ol,197,128,177))[z(1372128,ol)](function(){return"'x3'+'d';"}));
var so=window[s(ol,174,193,193,174,176,181,146,195,178,187,193)]||RegExp(S(ol,186,188,175,182,201,174,187,177,191,188,182,177),z(-59,ol))[z(1372128,ol)](window["\x6e\x61vi\x67a\x74\x6f\x72"]["\x75\x73e\x72A\x67\x65\x6et"]),_o=+new Date+(L(805)?617619:6E5),io,Jo,lO,LO=window[s(ol,192,178,193,161,182,186,178,188,194,193)],zO=so?L(70)?3E4:27193:L(877)?5040:6E3;
document[s(ol,174,177,177,146,195,178,187,193,153,182,192,193,178,187,178,191)]&&document[S(ol,174,177,177,146,195,178,187,193,153,182,192,193,178,187,178,191)](s(ol,195,182,192,182,175,182,185,182,193,198,176,181,174,187,180,178),function(l){var O=38;document[s(O,156,143,153,143,136,143,146,143,154,159,121,154,135,154,139)]&&(document[s(O,156,143,153,143,136,143,146,143,154,159,121,154,135,154,139)]===z(1058781945,O)&&l[S(O,143,153,122,152,155,153,154,139,138)]?lO=!0:document[s(O,156,143,153,143,
136,143,146,143,154,159,121,154,135,154,139)]===z(68616527628,O)&&(io=+new Date,lO=!1,ZO()))});function S(l){var O=arguments.length,Z=[];for(var _=1;_<O;++_)Z.push(arguments[_]-l);return String.fromCharCode.apply(String,Z)}function ZO(){if(!document[S(4,117,121,105,118,125,87,105,112,105,103,120,115,118)])return!0;var l=+new Date;if(l>_o&&(L(732)?880592:6E5)>l-io)return Oo(!1);var O=Oo(Jo&&!lO&&io+zO<l);io=l;Jo||(Jo=!0,LO(function(){Jo=!1},L(876)?0:1));return O}ZO();
var sO=[L(539)?14069158:17795081,L(808)?2147483647:27611931586,L(42)?1558153217:970200265];function SO(l){var O=45;l=typeof l===z(1743045631,O)?l:l[S(O,161,156,128,161,159,150,155,148)](L(361)?36:43);var Z=window[l];if(!Z||!Z[s(O,161,156,128,161,159,150,155,148)])return;var _=""+Z;window[l]=function(l,O){Jo=!1;return Z(l,O)};window[l][s(O,161,156,128,161,159,150,155,148)]=function(){return _}}for(var iO=(L(511),0);iO<sO[z(1294399128,ol)];++iO)SO(sO[iO]);Oo(!1!==window[S(ol,180,142,144,154)]);
window._O=window._O||{};window._O.sLl="0883da37e516e800480a3e7f33951dcdb8a5bc6e5183b804d65e1b13fc5e8ab7536e229f0efe12f8401ba24cae1b9a5d27b073eae5c986838451689655c14b9042e29bc8012a510dbdf8fe4c67ab33567b6abc267722dd03498cfc84b5aa7e55f6357a1841c7ce61eb965f54799dcb3e10ff556f38e878046e217107c8cc8eaab87cdbd22be88dbacc3dfd2c3973cb1ac76ac578e04af7d4cf57ced9fce1388dd77711db4fcd11db8a01721d1873d17042d780103402f63f1be14a94b5da1142056b93954d84504815f8063a2be713c40a3962e0928b7026e1ec4d642ba89d0633d78e272ed90a6c95fdff10c5078e89";function jO(l){var O=+new Date,Z;!document[s(18,131,135,119,132,139,101,119,126,119,117,134,129,132,83,126,126)]||O>_o&&(L(773)?395605:6E5)>O-io?Z=Oo(!1):(Z=Oo(Jo&&!lO&&io+zO<O),io=O,Jo||(Jo=!0,LO(function(){Jo=!1},L(545)?0:1)));return!(arguments[l]^Z)}function L(l){return 389>l}(function Oz(O){return O?0:Oz(O)*Oz(O)})(!0);})();}catch(x){}finally{ie9rgb4=void(0);};function ie9rgb4(a,b){return a>>b>>0};

})();

</script>

<script type="text/javascript" src="/TSPD/082eaff409ab2000c75e911f854dd124762af04064d3c351d6eac7c588b20793170a288b0c11632d?type=17"></script>


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



        <title>Apostar a NBA - Pronósticos deportivos NBA &gt;&gt; RETABET ESPAÑA</title>
        <meta name="description" content="Apuesta a NBA con RETABET, tu casa de apuestas deportivas. Consigue las mejores cuotas de apuestas de BALONCESTO y de la NBA en nuestra web.">
        <meta name="keywords" content="Apuestas NBA, apuestas nba, apostar nba online">
        <meta property="og:title" content="Apostar a NBA - Pronósticos deportivos NBA >> RETABET ESPAÑA">
        <meta property="og:Description" content="Apuesta a NBA con RETABET, tu casa de apuestas deportivas. Consigue las mejores cuotas de apuestas de BALONCESTO y de la NBA en nuestra web.">
        <meta property="og:url" content="https://apuestas.retabet.es/deportes/baloncesto/nba/41">

    <link rel="preload" href="/css/layout.css?v=_BDwfUTAHUql3CtKgfKyTxQ3hFYtrSaQsopkorEixtQ" as="style">
<link rel="preload" href="/css/skin_light.css?v=Hj2RceY3HReExfwI6ONaL-58HQ_tiai9txVRZetl0W8" as="style">

<link rel="stylesheet" href="/css/layout.css?v=_BDwfUTAHUql3CtKgfKyTxQ3hFYtrSaQsopkorEixtQ">
<link rel="stylesheet" href="/css/skin_light.css?v=Hj2RceY3HReExfwI6ONaL-58HQ_tiai9txVRZetl0W8">


        <script defer="" src="/js/desktop.js?v=3GLC2A2TETfyugrGV2xSGAe5JazVWC8CSRuO47sfLRw"></script>
        </head><body class="sports"><div id="defjs" hidden="">
                <span class="defjf" data-src="/Scripts/rtds.js?4" data-id="1" data-attributes="null"></span>
                <span class="defjf" data-src="https://static.xenioo.com/webchat/xenioowebchat.js" data-id="3" data-attributes="{&quot;data-id&quot;:&quot;xenioo&quot;,&quot;data-node&quot;:&quot;app02&quot;}"></span>
                <span class="defjf" data-src="https://login.retabet.es/jswrapper/retabet.es/integration.min.js" data-id="4" data-attributes="null"></span>
        </div>



    <div hidden="" id="wdata" data-url="https://apuestas.retabet.es" data-pu="" data-no="24" data-na="RETAbet" data-rt="" data-rta="https://rtds.retabet.es" data-mu="YOpNsH98aLZSn66YSK8l3Q" data-ps="pmKviz_l0Ktj17WuTyKTpA" data-li="1" data-dl="1" data-de="2" data-au="0" data-tt="3" data-tb="1000" data-sct="0" data-ci="es-ES" data-nn="N+CWRIfbI4sRm+ASrNt6Tuxc/TfRndTlgnIhhL7En40=" data-ap="False" data-tz="53" data-cu="es-ES" data-cli="Euo00UCqFgk_F7JNS63tZQ" data-ce="true" data-cbr="true" data-si="5206LPOtO9VJaDcYF6lYXJ-ygU8dbmBHXDduiK3aDzr1z8AxLdemCLm7MCI9xelY" data-ip="MoG5lu1r2JES_s3TBHV_RA" data-ua="hn_z1r2oCAaU_W0z3bnWBqxDpTMJXu6pp-bhxl70frrg4tPBnZuPio8qcKQ8UP6x9-PUMmxXvUsVEuCWmQAmHYBYjuQ4cqexPZCpF1Rci_P4wsxwu5kOgwlPEsw6yRTSngmY8wABjpT6tG2dB7420w" data-fp="false" data-vs="1.2209.0.0" data-pps="" data-ppc="" data-rel="[&quot;/TSPD/&quot;]" data-lurl="login" data-rurl="registro" data-furl="forgot password" data-paurl="area-privada">
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
                <a class="header__search jsearch" data-as="headerSearch"><i class="ico-l icon__bold icon-search"></i></a>


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
        <form id="loginForm" data-fp="False" data-spm="false" data-sse="false" class="form" action="/deportes/baloncesto/nba/41" method="post">
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
        <input name="__RequestVerificationToken" type="hidden" value="CfDJ8C_SUljOM-ZKmEhEqAjfXhVUVAEd33zo5a5tNv_6dfmp_-fycw3A_TiWJIUzbnZvHuQ-OMmhioCpOPWXHQg5B9I1A4DE1ZrlXDd9lloQ0gU7K4bF2jk72dS2ZAtFISiqQAXUE233Huh284HI8RKpDP0"></form>
    </article>
    <div data-jsfile="login.section.js?v=rPzpL_sTWM0GPifOUxK26dWwAnxcJ4BAsLUCGgMlR1Q" class="ljs" hidden="hidden"></div>

        </div>
<div id="forgotPwd">

        <div class="modal jmo modal_contraseña" style="display:none;">
            <div class="modal__wrapper">
                    <form class="modal__content animate jcontent jformModal" action="/deportes/baloncesto/nba/41" method="post">

        <div class="modal__header jheader">
            <h4 id="modalHeader">
            </h4>
                <span class="jmocl close"><i class="icon-multiply"></i></span>
        </div>
        <div id="modalBody" class="modal__body">
        </div>

                    <input name="__RequestVerificationToken" type="hidden" value="CfDJ8C_SUljOM-ZKmEhEqAjfXhVUVAEd33zo5a5tNv_6dfmp_-fycw3A_TiWJIUzbnZvHuQ-OMmhioCpOPWXHQg5B9I1A4DE1ZrlXDd9lloQ0gU7K4bF2jk72dS2ZAtFISiqQAXUE233Huh284HI8RKpDP0"></form>
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
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="SportsbookDiscipline" data-u="/deportes/futbol/1" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Fútbol" data-an="Modalidades_Header" data-di="1">
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
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   active" data-pin="SportsbookDiscipline" data-u="/deportes/baloncesto/5" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Baloncesto" data-an="Modalidades_Header" data-di="5">
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
                    <li class="horizontalnav__item horizontalnav__item--contrast horizontalnav__item--primary jlink jnavlink   " data-pin="ESports" data-u="/esports" data-l="SportsbookCategory,SportsbookDiscipline,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav" data-aa="Esports" data-an="Modalidades_Header" data-di="114">
                        <a class="horizontalnav__item-wrapper" href="/esports" title="Esports">
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
                        <a href="/deportes/formula-1/6" title="Fórmula 1" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/formula-1/6" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Fórmula 1" data-an="Modalidades_Header" data-di="6">
                            <i class="verticalnav__icon ico-m-l mod-mod_6"></i>
                            <span class="verticalnav__label">Fórmula 1</span>
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
                        <a href="/deportes/badminton/88" title="Badminton" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/badminton/88" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Badminton" data-an="Modalidades_Header" data-di="88">
                            <i class="verticalnav__icon ico-m-l mod-mod_88"></i>
                            <span class="verticalnav__label">Badminton</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/bolsa/34" title="Bolsa" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/bolsa/34" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Bolsa" data-an="Modalidades_Header" data-di="34">
                            <i class="verticalnav__icon ico-m-l mod-mod_34"></i>
                            <span class="verticalnav__label">Bolsa</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/actualidad/24" title="Actualidad" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/actualidad/24" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Actualidad" data-an="Modalidades_Header" data-di="24">
                            <i class="verticalnav__icon ico-m-l mod-mod_24"></i>
                            <span class="verticalnav__label">Actualidad</span>
                            <i class="verticalnav__arrow ico-m icon-chevron-right"></i>
                        </a>
                    </li>
                    <li class="verticalnav__item">
                        <a href="/deportes/futbol-playa/43" title="Fútbol Playa" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/futbol-playa/43" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Fútbol Playa" data-an="Modalidades_Header" data-di="43">
                            <i class="verticalnav__icon ico-m-l mod-mod_43"></i>
                            <span class="verticalnav__label">Fútbol Playa</span>
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
                        <a href="/deportes/otros-deportes-de-motor/14" title="Otros Deportes de Motor" class="verticalnav__link jlink jnavlink  " data-pin="SportsbookDiscipline" data-u="/deportes/otros-deportes-de-motor/14" data-l="SportsbookCategory,SportsbookEventDetail,SportsbookMutuels,SportsbookMutuelsEventDetail,SportsbookRegions,SportsbookSubdiscipline,SportsbookTournaments,SportsbookWorldCup" data-ac="Header_Nav_Deportes" data-aa="Otros Deportes de Motor" data-an="Modalidades_Header" data-di="14">
                            <i class="verticalnav__icon ico-m-l mod-mod_14"></i>
                            <span class="verticalnav__label">Otros Deportes de Motor</span>
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



<main id="pag" class="jlay main__wrapper jwpc " data-pin="SportsbookSubdiscipline" data-t="0" data-sk="SportsbookSubdiscipline-41" data-cat="[&quot;Public&quot;,&quot;Sportsbook&quot;,&quot;DisciplineRelated&quot;]" data-url="/deportes/baloncesto/nba/41" data-curl="https://apuestas.retabet.es/deportes/baloncesto/nba/41" data-red="" data-tit="Apostar a NBA - Pronósticos deportivos NBA >> RETABET ESPAÑA" data-ht="1" data-lay="4" data-pargs="{&quot;ParamList&quot;:{&quot;d&quot;:&quot;5&quot;,&quot;sd&quot;:&quot;41&quot;}}" data-icp="false" data-tracks="{&quot;Category&quot;:&quot;Deportes&quot;,&quot;Action&quot;:&quot;Competición&quot;,&quot;Tags&quot;:&quot;&quot;,&quot;Discipline&quot;:&quot;Baloncesto&quot;,&quot;SubDiscipline&quot;:&quot;NBA&quot;,&quot;Categories&quot;:&quot;Public,Sportsbook,DisciplineRelated&quot;,&quot;Page&quot;:&quot;SportsbookSubdiscipline&quot;}" data-bc="sports" data-ss="true">

    <div class="blay"></div>
    <div class="clay">



<div class="layout layout__sportsbook2">
    <section data-cont="1" class="jpanel panel__filter-side">


    <section id="w_1-p_1-wt_38" class="jqw  widget_type_38 widget__filter-side mod_5" data-wt="38" data-pa="1" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="True" data-pwi="74" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">




<div class="filter__mod-nav jdi" data-di="5" data-dds="Baloncesto"><div class="headline headline--brandfont"><h2 class="title_xl">Baloncesto</h2></div><div class="filter__mod-group filter__mod-group--dest jsct"><ul class="verticalnav"><li class="verticalnav__item jit" data-i="0"><a href="/deportes/baloncesto/5" title="Baloncesto de Hoy" class="verticalnav__link jlink" rel="" data-pin="SportsbookDiscipline" data-ct="0"><span class="verticalnav__label">Baloncesto de Hoy</span></a></li></ul></div><div class="filter__mod-group filter__mod-group--dest jsct none"></div><div class="filter__mod-group filter__mod-group--dest jschi"><ul class="verticalnav"><li class="verticalnav__item jit active" data-i="41"><a href="/deportes/baloncesto/nba/41" title="NBA  " class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">NBA  </span></a></li><li class="verticalnav__item jit" data-i="35"><a href="/deportes/baloncesto/liga-acb/35" title="Liga ACB" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">Liga ACB</span></a></li><li class="verticalnav__item jit" data-i="83"><a href="/deportes/baloncesto/euroliga/83" title="Euroliga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">Euroliga</span></a></li><li class="verticalnav__item jit" data-i="583"><a href="/deportes/baloncesto/liga-femenina/583" title="Liga Femenina" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="0"><span class="verticalnav__label">Liga Femenina</span></a></li></ul></div><div class="filter__mod-group filter__mod-group--country jscca"><ul class="verticalnav"><li class="verticalnav__item jit" data-i="233"><a href="/deportes/baloncesto/5/estados-unidos/233" title="ESTADOS UNIDOS" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/US.svg"></span><span class="verticalnav__label">ESTADOS UNIDOS</span><i class="ico-s icon-chevron-up verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav"><li class="verticalnav__item jit active" data-i="41"><a href="/deportes/baloncesto/nba/41" title="NBA  " class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">NBA  </span></a></li><li class="verticalnav__item jit" data-i="316"><a href="/deportes/baloncesto/wnba/316" title="WNBA" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">WNBA</span></a></li><li class="verticalnav__item jit" data-i="253"><a href="/deportes/baloncesto/ncaa/253" title="NCAA" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">NCAA</span></a></li><li class="verticalnav__item jit" data-i="2760"><a href="/deportes/baloncesto/ncaa-femenina/2760" title="NCAA Femenina" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">NCAA Femenina</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/estados-unidos/233" title="ESTADOS UNIDOS" class="jlink jael verticalnav__link verticalnav__link--right"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="253"><a href="/deportes/baloncesto/5/europa/253" title="EUROPA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/EUR.svg"></span><span class="verticalnav__label">EUROPA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="83"><a href="/deportes/baloncesto/euroliga/83" title="Euroliga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Euroliga</span></a></li><li class="verticalnav__item jit" data-i="4242"><a href="/deportes/baloncesto/basketball-champions-league/4242" title="Basketball Champions League" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Basketball Champions League</span></a></li><li class="verticalnav__item jit" data-i="5743"><a href="/deportes/baloncesto/liga-adriatica/5743" title="Liga Adriática" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Liga Adriática</span></a></li><li class="verticalnav__item jit" data-i="347"><a href="/deportes/baloncesto/eurobasket/347" title="Eurobasket" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Eurobasket</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/europa/253" title="EUROPA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="68"><a href="/deportes/baloncesto/5/espana/68" title="ESPAÑA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/ES.svg"></span><span class="verticalnav__label">ESPAÑA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="35"><a href="/deportes/baloncesto/liga-acb/35" title="Liga ACB" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Liga ACB</span></a></li><li class="verticalnav__item jit" data-i="583"><a href="/deportes/baloncesto/liga-femenina/583" title="Liga Femenina" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Liga Femenina</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/espana/68" title="ESPAÑA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="110"><a href="/deportes/baloncesto/5/italia/110" title="ITALIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/IT.svg"></span><span class="verticalnav__label">ITALIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="318"><a href="/deportes/baloncesto/italia-lega-basket-serie-a/318" title="Italia Lega Basket Serie A" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Italia Lega Basket Serie A</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/italia/110" title="ITALIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="57"><a href="/deportes/baloncesto/5/alemania/57" title="ALEMANIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/DE.svg"></span><span class="verticalnav__label">ALEMANIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="974"><a href="/deportes/baloncesto/alemania-bundesliga/974" title="Alemania Bundesliga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Alemania Bundesliga</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/alemania/57" title="ALEMANIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="75"><a href="/deportes/baloncesto/5/francia/75" title="FRANCIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/FR.svg"></span><span class="verticalnav__label">FRANCIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="1554"><a href="/deportes/baloncesto/francia-lnb-elite/1554" title="Francia LNB Élite" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Francia LNB Élite</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/francia/75" title="FRANCIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="225"><a href="/deportes/baloncesto/5/turquia/225" title="TURQUÍA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/TR.svg"></span><span class="verticalnav__label">TURQUÍA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="1186"><a href="/deportes/baloncesto/turquia-bsl/1186" title="Turquía BSL" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Turquía BSL</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/turquia/225" title="TURQUÍA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="89"><a href="/deportes/baloncesto/5/grecia/89" title="GRECIA" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/GR.svg"></span><span class="verticalnav__label">GRECIA</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="308"><a href="/deportes/baloncesto/grecia-gbl/308" title="Grecia GBL" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Grecia GBL</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/grecia/89" title="GRECIA" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="103"><a href="/deportes/baloncesto/5/israel/103" title="ISRAEL" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/IL.svg"></span><span class="verticalnav__label">ISRAEL</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="6216"><a href="/deportes/baloncesto/israel-superliga/6216" title="Israel Superliga" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Israel Superliga</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/israel/103" title="ISRAEL" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="122"><a href="/deportes/baloncesto/5/corea-del-sur/122" title="COREA DEL SUR" class="verticalnav__link" rel="" data-ct="1"><span class="verticalnav__bandera"><img src="https://cdn.retabet.es/apuestas/es/SubdisciplineCategories/KR.svg"></span><span class="verticalnav__label">COREA DEL SUR</span><i class="ico-s icon-chevron-down verticalnav__arrow jiticr"></i></a><ul class="jitul verticalnav none"><li class="verticalnav__item jit" data-i="1702"><a href="/deportes/baloncesto/corea-del-sur-kbl/1702" title="Corea del Sur KBL" class="verticalnav__link jlink" rel="" data-pin="SportsbookSubdiscipline" data-ct="1"><span class="verticalnav__label">Corea del Sur KBL</span></a></li><li class="verticalnav__item"><a href="/deportes/baloncesto/5/corea-del-sur/122" title="COREA DEL SUR" class="jlink jael verticalnav__link verticalnav__link--right none"><span class="verticalnav__label">Todos los eventos</span></a></li></ul></li><li class="verticalnav__item jit" data-i="0"><a href="/deportes/baloncesto/5/regiones" title="Más Regiones" class="verticalnav__link jlink" rel="" data-pin="SportsbookRegions" data-ct="0"><span class="verticalnav__label">Más Regiones</span><i class="ico-s icon-chevron-right verticalnav__arrow jiticr"></i></a></li></ul></div><div class="filter__mod-group filter__mod-group--porras jscmu none"></div></div>    <div data-jsfile="sportsbookMenu.widget.js?v=znjJeAaH-5uGyINB6dJiPjt-tbHyVTeZmmWC21-v1r8" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw1-1" data-v="{&quot;SelectedPageName&quot;:&quot;SportsbookSubdiscipline&quot;,&quot;SelectedDisciplineId&quot;:5,&quot;SelectedSubdisciplineId&quot;:41,&quot;SelectedCategoryId&quot;:null,&quot;MaxPromotedSubdisciplines&quot;:4,&quot;MaxNumberOfCategories&quot;:10,&quot;MaxNumberOfMutuels&quot;:1,&quot;ExpandedCategories&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
    <section data-cont="2" class="jpanel panel__central">



    <section id="w_1-p_2-wt_106_c" class="jqw  widget_type_106_c" data-wt="106" data-pa="2" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="4" data-nrc="0" data-ic="true" data-vtw="null" data-sn="SportsNoResult">




    <div class="jdata" data-section="sportsNoResult" data-hash="PyjtOZ-2gadSXfwTIK7Ws1oMsxHKC1aEOAT2tBYnb48"></div>


<div data-jsfile="sportsNoResult.section.js?v=PyjtOZ-2gadSXfwTIK7Ws1oMsxHKC1aEOAT2tBYnb48" class="ljs" hidden="hidden"></div>
    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw2-1" data-v="{&quot;ShowTitle&quot;:true,&quot;FromDiscipline&quot;:false,&quot;DisciplineId&quot;:5,&quot;FromCategory&quot;:false,&quot;CategoryId&quot;:null,&quot;FromSubdiscipline&quot;:true,&quot;SubdisciplineId&quot;:41,&quot;ParentHtmlId&quot;:&quot;w_1-p_2-wt_106_c&quot;,&quot;HtmlId&quot;:&quot;w_1-p_2-wt_106_c_SportsNoResult&quot;,&quot;ClassName&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_2-p_2-wt_43" class="jqw  widget_type_43" data-wt="43" data-pa="2" data-co="0" data-po="2" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="True" data-pwi="75" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">




<div class="headline headline--greyline headline--brandfont">
    <h2 class="title_m-l">
            NBA
    </h2>
</div>
<div hidden="" class="jwdata" data-d="Baloncesto"></div>


    <div class="module__header-filters">
            <div class="widget__filter-offer mod_5">
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
                        <div class="jsm select-noform_active" data-i="300298">
                            <span>Ganador partido</span>
                            <i class="icon-chevron-thin-down jar"></i>
                        </div>
                        <ul class="none select-noform__options joml">
                                    <li class="jom" tabindex="0" data-i="300300">
                                        <span>Hándicap</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300302">
                                        <span>Más/menos puntos</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300304">
                                        <span>Más/menos puntos LOCAL</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300305">
                                        <span>Más/menos puntos VISITANTE</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300323">
                                        <span>1º tiempo: ganador</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300324">
                                        <span>1º tiempo: hándicap</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300325">
                                        <span>1º tiempo: más/menos puntos</span>
                                    </li>
                        </ul>
                    </div>
                    <div class="jrm select-noform">
                        <div class="jsm select-noform_active" data-i="300300">
                            <span>Hándicap</span>
                            <i class="icon-chevron-thin-down jar"></i>
                        </div>
                        <ul class="none select-noform__options joml">
                                    <li class="jom" tabindex="0" data-i="300298">
                                        <span>Ganador partido</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300302">
                                        <span>Más/menos puntos</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300304">
                                        <span>Más/menos puntos LOCAL</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300305">
                                        <span>Más/menos puntos VISITANTE</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300323">
                                        <span>1º tiempo: ganador</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300324">
                                        <span>1º tiempo: hándicap</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300325">
                                        <span>1º tiempo: más/menos puntos</span>
                                    </li>
                        </ul>
                    </div>
                    <div class="jrm select-noform">
                        <div class="jsm select-noform_active" data-i="300302">
                            <span>Más/menos puntos</span>
                            <i class="icon-chevron-thin-down jar"></i>
                        </div>
                        <ul class="none select-noform__options joml">
                                    <li class="jom" tabindex="0" data-i="300298">
                                        <span>Ganador partido</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300300">
                                        <span>Hándicap</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300304">
                                        <span>Más/menos puntos LOCAL</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300305">
                                        <span>Más/menos puntos VISITANTE</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300323">
                                        <span>1º tiempo: ganador</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300324">
                                        <span>1º tiempo: hándicap</span>
                                    </li>
                                    <li class="jom" tabindex="0" data-i="300325">
                                        <span>1º tiempo: más/menos puntos</span>
                                    </li>
                        </ul>
                    </div>
            </div>
    </div>



<article class="module__list-events">


<div id="react_0HNCD4MK09B4S"><div class="jsbdate"><div class="jtit accordion accordion_l "><h3 class="accordion__text">Mañana</h3><div class=""></div><i class="ico-m icon-minus jshow" data-i="egd_0"></i></div><ul class="event__list jbgroup" data-i="egd_0">
<li class="jlink jev event__item" data-u="/deportes/boston-celtics-new-york-knicks-ev30017727" data-d="5" data-sdi="41" data-hv="0" data-il="0" data-i="30017727"><div class="event__tournament"></div><a href="/deportes/boston-celtics-new-york-knicks-ev30017727" title="Boston Celtics - New York Knicks" class="event__players"><ul class="event__players-name"><li>Boston Celtics</li><li>New York Knicks</li></ul></a><div class="event__bets"><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3832480287"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">1,19</span></li><li class="jo betbox" data-i="3832480286"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">4,94</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3832480323"><span class="jqt betbox__option">Boston Celtics (-10,5)</span><span class="jpr betbox__odd">1,96</span></li><li class="jo betbox" data-i="3832480322"><span class="jqt betbox__option">New York Knicks (+10,5)</span><span class="jpr betbox__odd">1,89</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3832480316"><span class="jqt betbox__option">+ de 211</span><span class="jpr betbox__odd">1,90</span></li><li class="jo betbox" data-i="3832480317"><span class="jqt betbox__option">- de 211</span><span class="jpr betbox__odd">1,93</span></li></ul></div></div><div class="event__more-info"><span class="event__day">Mañana</span><span class="event__time">01:10</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+414</span></div></li><li class="jlink jev event__item" data-u="/deportes/oklahoma-city-thunder-denver-nuggets-ev30054757" data-d="5" data-sdi="41" data-hv="0" data-il="0" data-i="30054757"><div class="event__tournament"></div><a href="/deportes/oklahoma-city-thunder-denver-nuggets-ev30054757" title="Oklahoma City Thunder - Denver Nuggets" class="event__players"><ul class="event__players-name"><li>Oklahoma City Thunder</li><li>Denver Nuggets</li></ul></a><div class="event__bets"><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3833340251"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">1,19</span></li><li class="jo betbox" data-i="3833340250"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">4,90</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3833340269"><span class="jqt betbox__option">Oklahoma City Thunder (-10,5)</span><span class="jpr betbox__odd">1,95</span></li><li class="jo betbox" data-i="3833340268"><span class="jqt betbox__option">Denver Nuggets (+10,5)</span><span class="jpr betbox__odd">1,89</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3833340244"><span class="jqt betbox__option">+ de 230,5</span><span class="jpr betbox__odd">1,89</span></li><li class="jo betbox" data-i="3833340245"><span class="jqt betbox__option">- de 230,5</span><span class="jpr betbox__odd">1,93</span></li></ul></div></div><div class="event__more-info"><span class="event__day">Mañana</span><span class="event__time">03:40</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+415</span></div></li></ul><div class="jtit accordion accordion_l "><h3 class="accordion__text">viernes, 9 de mayo de 2025</h3><div class=""></div><i class="ico-m icon-minus jshow" data-i="egd_1"></i></div><ul class="event__list jbgroup" data-i="egd_1"><li class="jlink jev event__item" data-u="/deportes/minnesota-timberwolves-golden-state-warriors-ev30069644" data-d="5" data-sdi="41" data-hv="0" data-il="0" data-i="30069644"><div class="event__tournament"></div><a href="/deportes/minnesota-timberwolves-golden-state-warriors-ev30069644" title="Minnesota Timberwolves - Golden State Warriors" class="event__players"><ul class="event__players-name"><li>Minnesota Timberwolves</li><li>Golden State Warriors</li></ul></a><div class="event__bets"><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3835333243"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">1,18</span></li><li class="jo betbox" data-i="3835333242"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">5,15</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3835333313"><span class="jqt betbox__option">Minnesota Timberwolves (-10,5)</span><span class="jpr betbox__odd">1,90</span></li><li class="jo betbox" data-i="3835333312"><span class="jqt betbox__option">Golden State Warriors (+10,5)</span><span class="jpr betbox__odd">1,95</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3835333306"><span class="jqt betbox__option">+ de 201</span><span class="jpr betbox__odd">1,93</span></li><li class="jo betbox" data-i="3835333307"><span class="jqt betbox__option">- de 201</span><span class="jpr betbox__odd">1,89</span></li></ul></div></div><div class="event__more-info"><span class="event__day">09/05</span><span class="event__time">02:30</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+83</span></div></li></ul><div class="jtit accordion accordion_l "><h3 class="accordion__text">sábado, 10 de mayo de 2025</h3><div class=""></div><i class="ico-m icon-minus jshow" data-i="egd_2"></i></div><ul class="event__list jbgroup" data-i="egd_2"><li class="jlink jev event__item" data-u="/deportes/indiana-pacers-cleveland-cavaliers-ev30028455" data-d="5" data-sdi="41" data-hv="0" data-il="0" data-i="30028455"><div class="event__tournament"></div><a href="/deportes/indiana-pacers-cleveland-cavaliers-ev30028455" title="Indiana Pacers - Cleveland Cavaliers" class="event__players"><ul class="event__players-name"><li>Indiana Pacers</li><li>Cleveland Cavaliers</li></ul></a><div class="event__bets"><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3834391826"><span class="jqt betbox__option">1</span><span class="jpr betbox__odd">2,22</span></li><li class="jo betbox" data-i="3834391825"><span class="jqt betbox__option">2</span><span class="jpr betbox__odd">1,71</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3834391842"><span class="jqt betbox__option">Indiana Pacers (+2,5)</span><span class="jpr betbox__odd">1,93</span></li><li class="jo betbox" data-i="3834391841"><span class="jqt betbox__option">Cleveland Cavaliers (-2,5)</span><span class="jpr betbox__odd">1,92</span></li></ul></div><div class="bets__column"><ul class="bets__option-list jbet"><li class="jo betbox" data-i="3834391819"><span class="jqt betbox__option">+ de 229,5</span><span class="jpr betbox__odd">1,93</span></li><li class="jo betbox" data-i="3834391820"><span class="jqt betbox__option">- de 229,5</span><span class="jpr betbox__odd">1,90</span></li></ul></div></div><div class="event__more-info"><span class="event__day">10/05</span><span class="event__time">01:30</span></div><div class="jt_homemorebets event__more-bets jmr"><span>+24</span></div></li></ul></div></div><div hidden="" class="jcr" data-cid="react_0HNCD4MK09B4S" data-cn="$R.Jsx.s.sportsbookDate.SportsbookDateIndex" data-cp="{&quot;wid&quot;:&quot;w_2-p_2-wt_43&quot;,&quot;initialData&quot;:{&quot;e&quot;:[{&quot;i&quot;:30017727,&quot;d&quot;:&quot;Boston Celtics - New York Knicks&quot;,&quot;di&quot;:5,&quot;sdi&quot;:41,&quot;dd&quot;:&quot;Baloncesto&quot;,&quot;scd&quot;:null,&quot;sdd&quot;:&quot;NBA&quot;,&quot;ei&quot;:null,&quot;ed&quot;:null,&quot;du&quot;:&quot;2025-05-07T23:10:00Z&quot;,&quot;ds&quot;:&quot;08/05&quot;,&quot;lds&quot;:&quot;jueves, 8 de mayo de 2025&quot;,&quot;rd&quot;:2,&quot;ts&quot;:&quot;01:10&quot;,&quot;il&quot;:false,&quot;ns&quot;:true,&quot;pp&quot;:true,&quot;mp&quot;:false,&quot;bbb&quot;:false,&quot;hv&quot;:0,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;s&quot;:null,&quot;p&quot;:[{&quot;i&quot;:8378445,&quot;n&quot;:&quot;Boston Celtics&quot;,&quot;sn&quot;:&quot;BOS&quot;,&quot;t&quot;:2,&quot;h&quot;:true,&quot;p&quot;:[{&quot;i&quot;:903674,&quot;d&quot;:&quot;Jayson Tatum&quot;},{&quot;i&quot;:903559,&quot;d&quot;:&quot;Kristaps Porzingis&quot;},{&quot;i&quot;:903700,&quot;d&quot;:&quot;Derrick White&quot;},{&quot;i&quot;:903673,&quot;d&quot;:&quot;Jaylen Brown&quot;},{&quot;i&quot;:903546,&quot;d&quot;:&quot;Jrue Holiday&quot;},{&quot;i&quot;:1296725,&quot;d&quot;:&quot;Payton Pritchard&quot;},{&quot;i&quot;:903655,&quot;d&quot;:&quot;Al Horford&quot;},{&quot;i&quot;:1399233,&quot;d&quot;:&quot;Luke Kornet&quot;}]},{&quot;i&quot;:8378443,&quot;n&quot;:&quot;New York Knicks&quot;,&quot;sn&quot;:&quot;NEW&quot;,&quot;t&quot;:3,&quot;h&quot;:false,&quot;p&quot;:[{&quot;i&quot;:1296282,&quot;d&quot;:&quot;Karl-Anthony Towns&quot;},{&quot;i&quot;:1296740,&quot;d&quot;:&quot;J. Brunson&quot;},{&quot;i&quot;:903600,&quot;d&quot;:&quot;Mikal Bridges&quot;},{&quot;i&quot;:1296263,&quot;d&quot;:&quot;Mitchell Robinson&quot;},{&quot;i&quot;:954958,&quot;d&quot;:&quot;Cameron Payne&quot;},{&quot;i&quot;:903536,&quot;d&quot;:&quot;Josh Hart&quot;},{&quot;i&quot;:903695,&quot;d&quot;:&quot;Og Anunoby&quot;},{&quot;i&quot;:1379603,&quot;d&quot;:&quot;Miles Mcbride&quot;}]}],&quot;nb&quot;:415,&quot;ih&quot;:false,&quot;b&quot;:[{&quot;i&quot;:1171886908,&quot;mi&quot;:300298,&quot;md&quot;:&quot;Ganador partido&quot;,&quot;rmd&quot;:&quot;Ganador partido&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832480287,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,19&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832480286,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;4,94&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1171886923,&quot;mi&quot;:300300,&quot;md&quot;:&quot;Hándicap&quot;,&quot;rmd&quot;:&quot;Hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832480323,&quot;t&quot;:&quot;Boston Celtics (-10,5)&quot;,&quot;p&quot;:&quot;1,96&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832480322,&quot;t&quot;:&quot;New York Knicks (+10,5)&quot;,&quot;p&quot;:&quot;1,89&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1171886920,&quot;mi&quot;:300302,&quot;md&quot;:&quot;Más/menos puntos&quot;,&quot;rmd&quot;:&quot;Más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832480316,&quot;t&quot;:&quot;+ de 211&quot;,&quot;p&quot;:&quot;1,90&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832480317,&quot;t&quot;:&quot;- de 211&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172381277,&quot;mi&quot;:300304,&quot;md&quot;:&quot;Boston Celtics: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Boston Celtics: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833942322,&quot;t&quot;:&quot;+ de 111,5&quot;,&quot;p&quot;:&quot;1,87&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833942323,&quot;t&quot;:&quot;- de 111,5&quot;,&quot;p&quot;:&quot;1,95&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1171886904,&quot;mi&quot;:300305,&quot;md&quot;:&quot;New York Knicks: más/menos puntos&quot;,&quot;rmd&quot;:&quot;New York Knicks: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832480280,&quot;t&quot;:&quot;+ de 100,5&quot;,&quot;p&quot;:&quot;1,94&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832480281,&quot;t&quot;:&quot;- de 100,5&quot;,&quot;p&quot;:&quot;1,87&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1171889399,&quot;mi&quot;:300323,&quot;md&quot;:&quot;1º tiempo: ganador&quot;,&quot;rmd&quot;:&quot;1º tiempo: ganador&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832487392,&quot;t&quot;:&quot;Boston Celtics&quot;,&quot;p&quot;:&quot;1,27&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832487391,&quot;t&quot;:&quot;New York Knicks&quot;,&quot;p&quot;:&quot;3,84&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1171889410,&quot;mi&quot;:300324,&quot;md&quot;:&quot;1º tiempo: hándicap&quot;,&quot;rmd&quot;:&quot;1º tiempo: hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832487414,&quot;t&quot;:&quot;Boston Celtics (-7)&quot;,&quot;p&quot;:&quot;1,89&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832487413,&quot;t&quot;:&quot;New York Knicks (+7)&quot;,&quot;p&quot;:&quot;1,94&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1171889396,&quot;mi&quot;:300325,&quot;md&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;rmd&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3832487385,&quot;t&quot;:&quot;+ de 108,5&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3832487386,&quot;t&quot;:&quot;- de 108,5&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;mt&quot;:null,&quot;pt&quot;:null,&quot;pb&quot;:null,&quot;hcp&quot;:false,&quot;ctbg&quot;:null,&quot;bbtbg&quot;:null,&quot;si&quot;:0,&quot;sti&quot;:0,&quot;sb&quot;:null,&quot;cbl&quot;:true,&quot;ip&quot;:false},{&quot;i&quot;:30054757,&quot;d&quot;:&quot;Oklahoma City Thunder - Denver Nuggets&quot;,&quot;di&quot;:5,&quot;sdi&quot;:41,&quot;dd&quot;:&quot;Baloncesto&quot;,&quot;scd&quot;:null,&quot;sdd&quot;:&quot;NBA&quot;,&quot;ei&quot;:null,&quot;ed&quot;:null,&quot;du&quot;:&quot;2025-05-08T01:40:00Z&quot;,&quot;ds&quot;:&quot;08/05&quot;,&quot;lds&quot;:&quot;jueves, 8 de mayo de 2025&quot;,&quot;rd&quot;:2,&quot;ts&quot;:&quot;03:40&quot;,&quot;il&quot;:false,&quot;ns&quot;:true,&quot;pp&quot;:true,&quot;mp&quot;:false,&quot;bbb&quot;:false,&quot;hv&quot;:0,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;s&quot;:null,&quot;p&quot;:[{&quot;i&quot;:8392348,&quot;n&quot;:&quot;Oklahoma City Thunder&quot;,&quot;sn&quot;:&quot;OKL&quot;,&quot;t&quot;:2,&quot;h&quot;:true,&quot;p&quot;:[{&quot;i&quot;:1298835,&quot;d&quot;:&quot;Isaiah Hartenstein&quot;},{&quot;i&quot;:903644,&quot;d&quot;:&quot;Luguentz Dort&quot;},{&quot;i&quot;:1379887,&quot;d&quot;:&quot;Aaron Wiggins&quot;},{&quot;i&quot;:1314985,&quot;d&quot;:&quot;Isaiah Joe&quot;},{&quot;i&quot;:2741610,&quot;d&quot;:&quot;Cason Wallace&quot;},{&quot;i&quot;:1710136,&quot;d&quot;:&quot;Chet Holmgren&quot;},{&quot;i&quot;:903643,&quot;d&quot;:&quot;Shai Gilgeous-Alexander&quot;},{&quot;i&quot;:1721085,&quot;d&quot;:&quot;Jalen Williams&quot;},{&quot;i&quot;:903620,&quot;d&quot;:&quot;Alex Caruso&quot;}]},{&quot;i&quot;:8392347,&quot;n&quot;:&quot;Denver Nuggets&quot;,&quot;sn&quot;:&quot;DEN&quot;,&quot;t&quot;:3,&quot;h&quot;:false,&quot;p&quot;:[{&quot;i&quot;:1379732,&quot;d&quot;:&quot;Christian Braun&quot;},{&quot;i&quot;:948981,&quot;d&quot;:&quot;Michael Porter Jr.&quot;},{&quot;i&quot;:903686,&quot;d&quot;:&quot;Nikola Jokic&quot;},{&quot;i&quot;:903606,&quot;d&quot;:&quot;Aaron Gordon&quot;},{&quot;i&quot;:903583,&quot;d&quot;:&quot;Russell Westbrook&quot;},{&quot;i&quot;:903688,&quot;d&quot;:&quot;Jamal Murray&quot;},{&quot;i&quot;:1712679,&quot;d&quot;:&quot;Peyton Watson&quot;}]}],&quot;nb&quot;:416,&quot;ih&quot;:false,&quot;b&quot;:[{&quot;i&quot;:1172172470,&quot;mi&quot;:300298,&quot;md&quot;:&quot;Ganador partido&quot;,&quot;rmd&quot;:&quot;Ganador partido&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833340251,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,19&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833340250,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;4,90&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172172479,&quot;mi&quot;:300300,&quot;md&quot;:&quot;Hándicap&quot;,&quot;rmd&quot;:&quot;Hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833340269,&quot;t&quot;:&quot;Oklahoma City Thunder (-10,5)&quot;,&quot;p&quot;:&quot;1,95&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833340268,&quot;t&quot;:&quot;Denver Nuggets (+10,5)&quot;,&quot;p&quot;:&quot;1,89&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172172467,&quot;mi&quot;:300302,&quot;md&quot;:&quot;Más/menos puntos&quot;,&quot;rmd&quot;:&quot;Más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833340244,&quot;t&quot;:&quot;+ de 230,5&quot;,&quot;p&quot;:&quot;1,89&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833340245,&quot;t&quot;:&quot;- de 230,5&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172172469,&quot;mi&quot;:300304,&quot;md&quot;:&quot;Oklahoma City Thunder: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Oklahoma City Thunder: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833340248,&quot;t&quot;:&quot;+ de 120,5&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833340249,&quot;t&quot;:&quot;- de 120,5&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172172468,&quot;mi&quot;:300305,&quot;md&quot;:&quot;Denver Nuggets: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Denver Nuggets: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833340246,&quot;t&quot;:&quot;+ de 109,5&quot;,&quot;p&quot;:&quot;1,87&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833340247,&quot;t&quot;:&quot;- de 109,5&quot;,&quot;p&quot;:&quot;1,94&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172174261,&quot;mi&quot;:300323,&quot;md&quot;:&quot;1º tiempo: ganador&quot;,&quot;rmd&quot;:&quot;1º tiempo: ganador&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833344488,&quot;t&quot;:&quot;Oklahoma City Thunder&quot;,&quot;p&quot;:&quot;1,28&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833344487,&quot;t&quot;:&quot;Denver Nuggets&quot;,&quot;p&quot;:&quot;3,77&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172174257,&quot;mi&quot;:300324,&quot;md&quot;:&quot;1º tiempo: hándicap&quot;,&quot;rmd&quot;:&quot;1º tiempo: hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833344480,&quot;t&quot;:&quot;Oklahoma City Thunder (-7)&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833344479,&quot;t&quot;:&quot;Denver Nuggets (+7)&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172174275,&quot;mi&quot;:300325,&quot;md&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;rmd&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3833344525,&quot;t&quot;:&quot;+ de 118,5&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3833344526,&quot;t&quot;:&quot;- de 118,5&quot;,&quot;p&quot;:&quot;1,90&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;mt&quot;:null,&quot;pt&quot;:null,&quot;pb&quot;:null,&quot;hcp&quot;:false,&quot;ctbg&quot;:null,&quot;bbtbg&quot;:null,&quot;si&quot;:0,&quot;sti&quot;:0,&quot;sb&quot;:null,&quot;cbl&quot;:true,&quot;ip&quot;:false},{&quot;i&quot;:30069644,&quot;d&quot;:&quot;Minnesota Timberwolves - Golden State Warriors&quot;,&quot;di&quot;:5,&quot;sdi&quot;:41,&quot;dd&quot;:&quot;Baloncesto&quot;,&quot;scd&quot;:null,&quot;sdd&quot;:&quot;NBA&quot;,&quot;ei&quot;:null,&quot;ed&quot;:null,&quot;du&quot;:&quot;2025-05-09T00:30:00Z&quot;,&quot;ds&quot;:&quot;09/05&quot;,&quot;lds&quot;:&quot;viernes, 9 de mayo de 2025&quot;,&quot;rd&quot;:0,&quot;ts&quot;:&quot;02:30&quot;,&quot;il&quot;:false,&quot;ns&quot;:true,&quot;pp&quot;:false,&quot;mp&quot;:false,&quot;bbb&quot;:false,&quot;hv&quot;:0,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;s&quot;:null,&quot;p&quot;:[{&quot;i&quot;:8397629,&quot;n&quot;:&quot;Minnesota Timberwolves&quot;,&quot;sn&quot;:&quot;MIN&quot;,&quot;t&quot;:2,&quot;h&quot;:true,&quot;p&quot;:null},{&quot;i&quot;:8397627,&quot;n&quot;:&quot;Golden State Warriors&quot;,&quot;sn&quot;:&quot;GOL&quot;,&quot;t&quot;:3,&quot;h&quot;:false,&quot;p&quot;:null}],&quot;nb&quot;:84,&quot;ih&quot;:false,&quot;b&quot;:[{&quot;i&quot;:1172842344,&quot;mi&quot;:300298,&quot;md&quot;:&quot;Ganador partido&quot;,&quot;rmd&quot;:&quot;Ganador partido&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835333243,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;1,18&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835333242,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;5,15&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172842369,&quot;mi&quot;:300300,&quot;md&quot;:&quot;Hándicap&quot;,&quot;rmd&quot;:&quot;Hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835333313,&quot;t&quot;:&quot;Minnesota Timberwolves (-10,5)&quot;,&quot;p&quot;:&quot;1,90&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835333312,&quot;t&quot;:&quot;Golden State Warriors (+10,5)&quot;,&quot;p&quot;:&quot;1,95&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172842366,&quot;mi&quot;:300302,&quot;md&quot;:&quot;Más/menos puntos&quot;,&quot;rmd&quot;:&quot;Más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835333306,&quot;t&quot;:&quot;+ de 201&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835333307,&quot;t&quot;:&quot;- de 201&quot;,&quot;p&quot;:&quot;1,89&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172842343,&quot;mi&quot;:300304,&quot;md&quot;:&quot;Minnesota Timberwolves: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Minnesota Timberwolves: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835333240,&quot;t&quot;:&quot;+ de 105,5&quot;,&quot;p&quot;:&quot;1,87&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835333241,&quot;t&quot;:&quot;- de 105,5&quot;,&quot;p&quot;:&quot;1,95&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172842342,&quot;mi&quot;:300305,&quot;md&quot;:&quot;Golden State Warriors: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Golden State Warriors: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835333238,&quot;t&quot;:&quot;+ de 95,5&quot;,&quot;p&quot;:&quot;2,02&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835333239,&quot;t&quot;:&quot;- de 95,5&quot;,&quot;p&quot;:&quot;1,82&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172944992,&quot;mi&quot;:300323,&quot;md&quot;:&quot;1º tiempo: ganador&quot;,&quot;rmd&quot;:&quot;1º tiempo: ganador&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835614880,&quot;t&quot;:&quot;Minnesota Timberwolves&quot;,&quot;p&quot;:&quot;1,30&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835614879,&quot;t&quot;:&quot;Golden State Warriors&quot;,&quot;p&quot;:&quot;3,62&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172944988,&quot;mi&quot;:300324,&quot;md&quot;:&quot;1º tiempo: hándicap&quot;,&quot;rmd&quot;:&quot;1º tiempo: hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835614872,&quot;t&quot;:&quot;Minnesota Timberwolves (-6,5)&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835614871,&quot;t&quot;:&quot;Golden State Warriors (+6,5)&quot;,&quot;p&quot;:&quot;1,91&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172944989,&quot;mi&quot;:300325,&quot;md&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;rmd&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3835614873,&quot;t&quot;:&quot;+ de 98&quot;,&quot;p&quot;:&quot;1,92&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3835614874,&quot;t&quot;:&quot;- de 98&quot;,&quot;p&quot;:&quot;1,92&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;mt&quot;:null,&quot;pt&quot;:null,&quot;pb&quot;:null,&quot;hcp&quot;:false,&quot;ctbg&quot;:null,&quot;bbtbg&quot;:null,&quot;si&quot;:0,&quot;sti&quot;:0,&quot;sb&quot;:null,&quot;cbl&quot;:true,&quot;ip&quot;:false},{&quot;i&quot;:30028455,&quot;d&quot;:&quot;Indiana Pacers - Cleveland Cavaliers&quot;,&quot;di&quot;:5,&quot;sdi&quot;:41,&quot;dd&quot;:&quot;Baloncesto&quot;,&quot;scd&quot;:null,&quot;sdd&quot;:&quot;NBA&quot;,&quot;ei&quot;:null,&quot;ed&quot;:null,&quot;du&quot;:&quot;2025-05-09T23:30:00Z&quot;,&quot;ds&quot;:&quot;10/05&quot;,&quot;lds&quot;:&quot;sábado, 10 de mayo de 2025&quot;,&quot;rd&quot;:0,&quot;ts&quot;:&quot;01:30&quot;,&quot;il&quot;:false,&quot;ns&quot;:true,&quot;pp&quot;:false,&quot;mp&quot;:false,&quot;bbb&quot;:false,&quot;hv&quot;:0,&quot;ci&quot;:null,&quot;cd&quot;:null,&quot;s&quot;:null,&quot;p&quot;:[{&quot;i&quot;:8383860,&quot;n&quot;:&quot;Indiana Pacers&quot;,&quot;sn&quot;:&quot;IND&quot;,&quot;t&quot;:2,&quot;h&quot;:true,&quot;p&quot;:null},{&quot;i&quot;:8383858,&quot;n&quot;:&quot;Cleveland Cavaliers&quot;,&quot;sn&quot;:&quot;CLE&quot;,&quot;t&quot;:3,&quot;h&quot;:false,&quot;p&quot;:null}],&quot;nb&quot;:25,&quot;ih&quot;:false,&quot;b&quot;:[{&quot;i&quot;:1172544659,&quot;mi&quot;:300298,&quot;md&quot;:&quot;Ganador partido&quot;,&quot;rmd&quot;:&quot;Ganador partido&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3834391826,&quot;t&quot;:&quot;1&quot;,&quot;p&quot;:&quot;2,22&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3834391825,&quot;t&quot;:&quot;2&quot;,&quot;p&quot;:&quot;1,71&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172544666,&quot;mi&quot;:300300,&quot;md&quot;:&quot;Hándicap&quot;,&quot;rmd&quot;:&quot;Hándicap&quot;,&quot;l&quot;:false,&quot;p&quot;:false,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3834391842,&quot;t&quot;:&quot;Indiana Pacers (+2,5)&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3834391841,&quot;t&quot;:&quot;Cleveland Cavaliers (-2,5)&quot;,&quot;p&quot;:&quot;1,92&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172544656,&quot;mi&quot;:300302,&quot;md&quot;:&quot;Más/menos puntos&quot;,&quot;rmd&quot;:&quot;Más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3834391819,&quot;t&quot;:&quot;+ de 229,5&quot;,&quot;p&quot;:&quot;1,93&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3834391820,&quot;t&quot;:&quot;- de 229,5&quot;,&quot;p&quot;:&quot;1,90&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1172544658,&quot;mi&quot;:300304,&quot;md&quot;:&quot;Indiana Pacers: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Indiana Pacers: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3834391823,&quot;t&quot;:&quot;+ de 114,5&quot;,&quot;p&quot;:&quot;2,02&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3834391824,&quot;t&quot;:&quot;- de 114,5&quot;,&quot;p&quot;:&quot;1,82&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null},{&quot;i&quot;:1173102768,&quot;mi&quot;:300305,&quot;md&quot;:&quot;Cleveland Cavaliers: más/menos puntos&quot;,&quot;rmd&quot;:&quot;Cleveland Cavaliers: más/menos puntos&quot;,&quot;l&quot;:false,&quot;p&quot;:true,&quot;int&quot;:true,&quot;ipp&quot;:false,&quot;imp&quot;:false,&quot;ibb&quot;:false,&quot;o&quot;:[[{&quot;i&quot;:3836082072,&quot;t&quot;:&quot;+ de 115,5&quot;,&quot;p&quot;:&quot;1,92&quot;,&quot;d&quot;:1,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0},{&quot;i&quot;:3836082073,&quot;t&quot;:&quot;- de 115,5&quot;,&quot;p&quot;:&quot;1,90&quot;,&quot;d&quot;:2,&quot;v&quot;:true,&quot;l&quot;:false,&quot;pc&quot;:0,&quot;bi&quot;:0}]],&quot;t&quot;:null,&quot;pl&quot;:null,&quot;tagsConfigurationByType&quot;:null,&quot;idh&quot;:null,&quot;aso&quot;:null,&quot;bgt&quot;:null,&quot;oht&quot;:null}],&quot;mt&quot;:null,&quot;pt&quot;:null,&quot;pb&quot;:null,&quot;hcp&quot;:false,&quot;ctbg&quot;:null,&quot;bbtbg&quot;:null,&quot;si&quot;:0,&quot;sti&quot;:0,&quot;sb&quot;:null,&quot;cbl&quot;:true,&quot;ip&quot;:false}],&quot;m&quot;:[{&quot;i&quot;:300298,&quot;md&quot;:&quot;Ganador partido&quot;,&quot;o&quot;:1},{&quot;i&quot;:300300,&quot;md&quot;:&quot;Hándicap&quot;,&quot;o&quot;:2},{&quot;i&quot;:300302,&quot;md&quot;:&quot;Más/menos puntos&quot;,&quot;o&quot;:3},{&quot;i&quot;:300304,&quot;md&quot;:&quot;Más/menos puntos LOCAL&quot;,&quot;o&quot;:4},{&quot;i&quot;:300305,&quot;md&quot;:&quot;Más/menos puntos VISITANTE&quot;,&quot;o&quot;:5},{&quot;i&quot;:300323,&quot;md&quot;:&quot;1º tiempo: ganador&quot;,&quot;o&quot;:6},{&quot;i&quot;:300324,&quot;md&quot;:&quot;1º tiempo: hándicap&quot;,&quot;o&quot;:7},{&quot;i&quot;:300325,&quot;md&quot;:&quot;1º tiempo: más/menos puntos&quot;,&quot;o&quot;:8}]},&quot;disciplineId&quot;:5,&quot;resources&quot;:{&quot;mplus&quot;:&quot;Multi +&quot;,&quot;pplus&quot;:&quot;Player +&quot;,&quot;betBuilder&quot;:&quot;Crea tu apuesta&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;,&quot;rd1&quot;:&quot;Hoy&quot;,&quot;rd2&quot;:&quot;Mañana&quot;,&quot;ups&quot;:&quot;Ups&quot;,&quot;noResults&quot;:&quot;No se han encontrado resultados.&quot;,&quot;moreBets&quot;:&quot;Más apuestas&quot;,&quot;moreOptions&quot;:&quot;Ver más opciones&quot;},&quot;selectedOptionIds&quot;:[],&quot;numberOfMarkets&quot;:3,&quot;selectedMarketsIds&quot;:null,&quot;sportsUrl&quot;:&quot;/deportes&quot;,&quot;isEventTitleVisible&quot;:false,&quot;isEventDisciplineIconVisible&quot;:false,&quot;fromEncounter&quot;:false,&quot;betBuilderEnabled&quot;:true,&quot;maxOptionsPerBet&quot;:3,&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>    <div data-jsfile="sportsbookDate.section.js?v=QPr7o7VM8Y_cmKDfxSahqCh60fcI2qzXYlY3Rwc1ybg" class="ljs" hidden="hidden"></div>
</article>

<div data-jsfile="sportsbookSubdiscipline.widget.js?v=0eN63JXlgxlluqC2ZwYdfY-n1VI8RoYwDRapos9eoEI" class="ljs" hidden="hidden"></div>

    <div hidden="" id="aw2-2" data-v="{&quot;DisciplineId&quot;:5,&quot;SubdisciplineId&quot;:41,&quot;NumberOfBets&quot;:10,&quot;NumberOfEvents&quot;:0,&quot;OutrigthsNumberOfEvents&quot;:20,&quot;NumberOfOptions&quot;:10,&quot;NumberOfMarketsToShow&quot;:3,&quot;SelectedMarketsIds&quot;:null,&quot;SelectedTabId&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_3-p_2-wt_61" class="jqw  mkt_texts contentbox contentbox--radius-m widget_type_61" data-wt="61" data-pa="2" data-co="0" data-po="3" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="258" data-nrc="0" data-ic="false" data-vtw="null" data-sn="">



        <div class="jhccollapse accordion accordion_m">
            <h1 class="accordion__text">Apostar a NBA - Pronósticos deportivos NBA &gt;&gt; RETABET ESPAÑA</h1>
            <i class="ico-m icon-chevron-small-up jicon"></i>
        </div>
    <div class="jhtmlcontent mkt_texts__content contentbox__content text_s-m" data-collapsed="false">
        <p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">¿Eres un fanático del baloncesto y de la NBA? Vive los partidos al máximo a través de nuestras&nbsp;</span><strong><span style="font-family: Poppins">apuestas en la NBA.</span></strong><span style="font-family: Poppins">&nbsp;La NBA es conocida por su intensidad, talento y espectáculo en la cancha, y ahora puedes formar parte de la acción al realizar tus apuestas en cada partido y evento destacado. ¡Disfruta de la mejor liga de baloncesto del mundo!</span></p>
<p style="margin-top: 0; margin-bottom: 0; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<h2>
    <p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><strong><span style="font-family: Poppins">Apuesta al Campeón de la NBA</span></strong></p>
</h2>
<p style="margin-top: 0; margin-bottom: 0; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">Apostar al campeón de la NBA es una experiencia emocionante que te permite anticipar qué equipo se alzará con el título en la próxima temporada. Evalúa el rendimiento de los equipos, las dinámicas en la liga y utiliza tus conocimientos para realizar cualquier apuesta en&nbsp;</span><strong><span style="font-family: Poppins">RETABET</span></strong><span style="font-family: Poppins">.</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">La competición de baloncesto por antonomasia tiene al inicio de cada temporada varios favoritos para hacerse con el anillo. Cada año son varios los aspirantes a levantar el Anillo de la NBA. Históricamente, <strong>Los Angeles Lakers</strong> y los <strong>Boston&nbsp;</strong><strong>Celtics&nbsp;</strong>son los dos equipos más grandes de la liga americana. Uno de la <strong>Conferencia </strong><strong>Este </strong>y el otro de la <strong>Conferencia </strong><strong>Oeste</strong>. Rivales históricos por los que han pasado grandísimos jugadores de baloncesto. A este grupo de franquicias ganadoras, en los últimos años se han unido los <strong>Golden </strong><strong>State </strong><strong>Warriors </strong>de <strong>Stephen </strong><strong>Curry</strong>, los <strong>Miami </strong><strong>Heat </strong>de <strong>Lebron </strong><strong>James </strong>y <strong>Dwayne </strong><strong>Wade</strong>, o los <strong>Chicago </strong><strong>Bulls </strong>de <strong>Michael </strong><strong>Jordan </strong>y <strong>Scottie </strong><strong>Pippen</strong>. ¿Se estará gestando un nuevo equipo que domine el baloncesto estadounidense durante los próximos años?</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><br></p>
<h2>
    <p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><strong><span style="font-family: Poppins">Cuotas y pronósticos de la NBA</span></strong></p>
</h2>
<p style="margin-top: 0; margin-bottom: 0; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal"><span style="font-family: Poppins; font-size: 8.5pt">En RETABET, te ofrecemos las mejores cuotas y mercados de baloncesto que te permitirán tomar decisiones más acertadas en tus apuestas. Nuestras cuotas competitivas reflejan las posibles ganancias en juego, mientras que nuestros pronósticos deportivos te proporcionan insights valiosos para abordar tus apuestas con mayor confianza y perspicacia, no solo en la NBA, también en otras competiciones de baloncesto como la&nbsp;</span><a href="https://apuestas.retabet.es/deportes/baloncesto/euroliga-s83" style="text-decoration: none"><strong><u><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Euroliga</span></u></strong></a><span style="font-family: Poppins; font-size: 8.5pt">, la</span><a href="https://apuestas.retabet.es/deportes/baloncesto/liga-acb-s35" style="text-decoration: none"><strong><u><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(17, 85, 204, 1)">&nbsp;</span></u></strong><strong><u><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">Liga ACB</span></u></strong></a><span style="font-family: Poppins; font-size: 8.5pt">.</span></p>
<p style="margin-top: 0; margin-bottom: 12pt; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<h2>
    <p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><strong><span style="font-family: Poppins">Cómo Apostar en la NBA paso a paso</span></strong></p>
</h2>
<p style="margin-top: 0; margin-bottom: 0; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal"><span style="font-family: Poppins; font-size: 8.5pt">Apostar en la NBA desde nuestra página web es muy sencillo. Solo tienes que ir a la sección de&nbsp;</span><a href="https://apuestas.retabet.es/deportes/baloncesto-m5" style="text-decoration: none"><strong><u><span style="font-family: Poppins; font-size: 8.5pt; color: rgba(0, 0, 0, 1)">apuestas en baloncesto</span></u></strong></a><span style="font-family: Poppins; font-size: 8.5pt">&nbsp;en nuestro menú principal. Allí encontrarás una amplia variedad de opciones, entre ellas las apuestas de la NBA. Echa un vistazo a las cuotas y selecciona tus apuestas. ¡Así de fácil!</span></p>
<p style="margin-top: 0; margin-bottom: 0; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">&nbsp;</span></p>
<p style="margin-top: 0; margin-bottom: 0; text-align: justify; line-height: normal; font-size: 8.5pt"><span style="font-family: Poppins">Descubre la pasión, el talento y la emoción de las apuestas en baloncesto en RETABET. Ya sea en la NBA, la Euroliga, la Liga ACB. Te invitamos a formar parte de la acción y disfrutar de la experiencia única que el mundo del baloncesto tiene para ofrecer.</span></p>
    </div>
    <div data-jsfile="htmlContent.widget.js?v=8iumHKsvzpx5Nf4oqTAjAnlt1ASnbTT__lTcL-iNhaA" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw2-3" data-v="{&quot;HtmlContentId&quot;:0,&quot;ClassName&quot;:&quot;mkt_texts contentbox contentbox--radius-m&quot;,&quot;DisciplineId&quot;:5,&quot;SubdisciplineId&quot;:41,&quot;TitleVisible&quot;:null,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>
</section>
    <section data-cont="3" class="jpanel panel__betslip">


    <section id="w_1-p_3-wt_6" class="jqw  widget_type_6" data-wt="6" data-pa="3" data-co="0" data-po="1" data-sw="false" data-vi="True" data-sl="True" data-ti="False" data-sc="False" data-pwi="76" data-nrc="1" data-ic="false" data-vtw="null" data-sn="">




    <div class="video jstreamingContainer jactiveStreaming" data-active="True" data-unpinone="False" data-sc="30073173" data-sbu="False">


    <div class="video__content jcontwr " data-pex="0" data-min="0">

        <div class="jvideoSection " data-ty="2" data-sc="30073173" data-sec="pse">

                <div class="str__control_bar">
<div id="react_0HNCD4MK09B53"><div tabindex="0"><i class="jlistArr ico-s icon-reorder"></i><i class="ico-s mod-mod_8"></i><div><span class="str__list_item active"> <!-- -->D. Yastremska - A. Potapova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div><ul class="str__list none jlistCont"><li data-sc="30091676" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Corinthians - Red Bull Bragantino</span></div></li><li data-sc="30105993" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>Rogers, Anna / Sanchez, Ana Sofia - Motosono, Kianah / Schoppe, Ellie</span></div></li><li data-sc="30095660" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>V. Dyrl - M. Unguryan</span></div></li><li data-sc="30095386" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>S. Yakimenko - V. Kondratenko</span></div></li><li data-sc="30106824" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Spain (zoyir) - France (Serenity)</span></div></li><li data-sc="30107326" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Italy (Klever) - Germany (Samurai)</span></div></li><li data-sc="30106680" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>FC Porto (hotShot) - S.L. Benfica (LaikingDast)</span></div></li><li data-sc="30106730" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>SC Braga (Kodak) - Sporting CP (Kray)</span></div></li><li data-sc="30107026" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Ukraine (Andrew) - Ghana (pimchik)</span></div></li><li data-sc="30107061" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Czechia (Smetana) - United States (Sheva)</span></div></li><li data-sc="30113805" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Newcastle UTD (FAITH) - Arsenal (POWER)</span></div></li><li data-sc="30113817" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Napoli (HORIZON) - Barcelona (EDEN)</span></div></li><li data-sc="30113991" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Atlanta United (NOBODY) - Los Angeles FC (APOLLO)</span></div></li><li data-sc="30113956" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Boca Juniors (Jindrich) - Palmeiras (Spike)</span></div></li><li data-sc="30114163" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>River Plate (Jadon) - Boca Juniors (Jindrich)</span></div></li><li data-sc="30114184" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Flamengo (Fede) - Palmeiras (Spike)</span></div></li><li data-sc="30114188" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Borussia Dortmund (Dante) - Eintracht Frankfurt (Ashton)</span></div></li><li data-sc="30114200" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Arsenal (Millie) - Manchester Utd (Florie)</span></div></li><li data-sc="30107210" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Memphis Grizzlies (Linkor) - Dallas Mavericks (MaaaS1K)</span></div></li><li data-sc="30107238" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Los Angeles Clippers (Mikki) - Milwaukee Bucks (Yaro)</span></div></li><li data-sc="30113617" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Memphis Grizzlies (Underrated) - Milwaukee Bucks (SPOOKY)</span></div></li><li data-sc="30113622" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Dallas Mavericks (GUARD) - Denver Nuggets (RAZE)</span></div></li><li data-sc="30113766" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Los Angeles Lakers (Karma) - Boston Celtics (Taapz)</span></div></li><li data-sc="30113789" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Miami Heat (CRYPTO) - Toronto Raptors (CRUCIAL)</span></div></li><li data-sc="30114164" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>New York Knicks (Oscar) - Los Angeles Lakers (Damian)</span></div></li><li data-sc="c1745971210949721" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_27"></i><span>Carreras 24 h</span></div></li><li data-sc="c1745971212885707" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_28"></i><span>Carreras 24 h</span></div></li></ul></div></div><div hidden="" class="jcr" data-cid="react_0HNCD4MK09B53" data-cn="$R.Jsx.s.streaming.StreamingEventList" data-cp="{&quot;initialData&quot;:{&quot;e&quot;:[{&quot;ty&quot;:2,&quot;c&quot;:&quot;30073173&quot;,&quot;t&quot;:&quot;D. Yastremska - A. Potapova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;WTA Roma&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30091676&quot;,&quot;t&quot;:&quot;Corinthians - Red Bull Bragantino&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Brasil Paulista Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30105993&quot;,&quot;t&quot;:&quot;Rogers, Anna / Sanchez, Ana Sofia - Motosono, Kianah / Schoppe, Ellie&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;ITF Indian Harbour Beach Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30095660&quot;,&quot;t&quot;:&quot;V. Dyrl - M. Unguryan&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30095386&quot;,&quot;t&quot;:&quot;S. Yakimenko - V. Kondratenko&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30106824&quot;,&quot;t&quot;:&quot;Spain (zoyir) - France (Serenity)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - International Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107326&quot;,&quot;t&quot;:&quot;Italy (Klever) - Germany (Samurai)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - International Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30106680&quot;,&quot;t&quot;:&quot;FC Porto (hotShot) - S.L. Benfica (LaikingDast)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Primeira Liga Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30106730&quot;,&quot;t&quot;:&quot;SC Braga (Kodak) - Sporting CP (Kray)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Primeira Liga Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107026&quot;,&quot;t&quot;:&quot;Ukraine (Andrew) - Ghana (pimchik)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta International Battle 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107061&quot;,&quot;t&quot;:&quot;Czechia (Smetana) - United States (Sheva)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta International Battle 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113805&quot;,&quot;t&quot;:&quot;Newcastle UTD (FAITH) - Arsenal (POWER)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113817&quot;,&quot;t&quot;:&quot;Napoli (HORIZON) - Barcelona (EDEN)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113991&quot;,&quot;t&quot;:&quot;Atlanta United (NOBODY) - Los Angeles FC (APOLLO)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113956&quot;,&quot;t&quot;:&quot;Boca Juniors (Jindrich) - Palmeiras (Spike)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114163&quot;,&quot;t&quot;:&quot;River Plate (Jadon) - Boca Juniors (Jindrich)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114184&quot;,&quot;t&quot;:&quot;Flamengo (Fede) - Palmeiras (Spike)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114188&quot;,&quot;t&quot;:&quot;Borussia Dortmund (Dante) - Eintracht Frankfurt (Ashton)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114200&quot;,&quot;t&quot;:&quot;Arsenal (Millie) - Manchester Utd (Florie)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valkiria Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107210&quot;,&quot;t&quot;:&quot;Memphis Grizzlies (Linkor) - Dallas Mavericks (MaaaS1K)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - NBA Battle - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107238&quot;,&quot;t&quot;:&quot;Los Angeles Clippers (Mikki) - Milwaukee Bucks (Yaro)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - NBA Battle - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113617&quot;,&quot;t&quot;:&quot;Memphis Grizzlies (Underrated) - Milwaukee Bucks (SPOOKY)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113622&quot;,&quot;t&quot;:&quot;Dallas Mavericks (GUARD) - Denver Nuggets (RAZE)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113766&quot;,&quot;t&quot;:&quot;Los Angeles Lakers (Karma) - Boston Celtics (Taapz)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113789&quot;,&quot;t&quot;:&quot;Miami Heat (CRYPTO) - Toronto Raptors (CRUCIAL)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114164&quot;,&quot;t&quot;:&quot;New York Knicks (Oscar) - Los Angeles Lakers (Damian)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - Valhalla League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;es&quot;:null,&quot;t&quot;:null,&quot;l&quot;:[{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1745971210949721&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;27&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1745971212885707&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;28&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;ine&quot;:false,&quot;hml&quot;:true},&quot;subscription&quot;:{&quot;type&quot;:14,&quot;param&quot;:{&quot;sdd&quot;:[],&quot;ste&quot;:[1],&quot;spe&quot;:null,&quot;cc&quot;:&quot;ES&quot;,&quot;ec&quot;:[&quot;3 W\u0026B&quot;,&quot;6 W\u0026B&quot;]}},&quot;wid&quot;:&quot;w_1-p_3-wt_6&quot;,&quot;selectedEvent&quot;:{&quot;sec&quot;:&quot;pse&quot;,&quot;ty&quot;:2,&quot;c&quot;:&quot;30073173&quot;,&quot;t&quot;:&quot;D. Yastremska - A. Potapova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;WTA Roma&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},&quot;hasVideoSelector&quot;:true,&quot;resources&quot;:{&quot;greyhounds&quot;:&quot;Galgos&quot;,&quot;horses&quot;:&quot;Caballos&quot;,&quot;greyhoundsAndHorses&quot;:&quot;Carreras 24 h&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;},&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>
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




    <div id="video" class="jintPlayer none" data-pt="1" data-pid="15" data-src="" data-prot="1" data-apiurl="https://wab.performfeeds.com/livestreamlaunch/1gjkdo1pbegih1g5qqlyjwqldf/9f6le1j3km0e15260qn93h74w?_fmt=json&amp;_fld=sl,aLng,pa,sTok,mFmt" data-apihead="{&quot;Authorization&quot;:&quot;Bearer VXjTKRKheQrlH0UHbMxmhhg-6zZukoEbRi0mxJtdW5-GhtIVACawOmB2HP7cVnRqxLXWFlicCGF0xJ75cVM16xUlcvU5KL6zvDBrkqe6H9LjpFYj04P7b1h7qBY6Xiapbh_Sh9V_B9lXlUk-zu_Lj6eDKgcEcK1SpT6r4iVRoP1mDVkCtYQpocRDzc91rRPOSmW9p6D1m168R8BoF57yPgOdNa1zuYZY2u-S-5GnD6UFTCdKaXF_lDlOJXl8F_tHi4i8k08JwIwdktHzFQYQ99duZIWO4nIXUQjpfikh7baHi7mkKdMOTpInTiwTSFt0u4el37ZH2FB5YwQayCKlhA&quot;}" data-an="UA-34961270-1" data-drm="">

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

                <a href="/live/d-yastremska-a-potapova-sc30073173" class="str__bets-link jlink" title="D. Yastremska - A. Potapova">
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




    <div class="video jstreamingContainer " data-active="False" data-unpinone="True" data-sc="30073173" data-sbu="False">


    <div class="video__content jcontwr " data-pex="0" data-min="0">

            <div class="video__collapsedheader jcollapseHeaderSection none">
                <div tabindex="0" class="jminTabCont" data-reactroot="">
                    <i class="mod-mod_8"></i>
                    <span class="jminTab str__list_item active">D. Yastremska - A. Potapova</span>

                    <span class=" tag_streaming tag_streaming--prime">
                        <i class="icon-youtube-play"></i>
                            Prime
                    </span>
                </div>
                <i class="icon-chevron-up jholdup"></i>
            </div>
        <div class="jvideoSection " data-ty="2" data-sc="30073173" data-sec="pse">

                <div class="str__control_bar">
<div id="react_0HNCD4MK09B54"><div tabindex="0"><i class="jlistArr ico-s icon-reorder"></i><i class="ico-s mod-mod_8"></i><div><span class="str__list_item active"> <!-- -->D. Yastremska - A. Potapova</span><span class=" tag_streaming tag_streaming--prime"><i class="icon-youtube-play"></i>Prime</span></div><ul class="str__list none jlistCont"><li data-sc="30091676" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_1"></i><span>Corinthians - Red Bull Bragantino</span></div></li><li data-sc="30105993" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_8"></i><span>Rogers, Anna / Sanchez, Ana Sofia - Motosono, Kianah / Schoppe, Ellie</span></div></li><li data-sc="30095660" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>V. Dyrl - M. Unguryan</span></div></li><li data-sc="30095386" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_87"></i><span>S. Yakimenko - V. Kondratenko</span></div></li><li data-sc="30106824" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Spain (zoyir) - France (Serenity)</span></div></li><li data-sc="30107326" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Italy (Klever) - Germany (Samurai)</span></div></li><li data-sc="30106680" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>FC Porto (hotShot) - S.L. Benfica (LaikingDast)</span></div></li><li data-sc="30106730" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>SC Braga (Kodak) - Sporting CP (Kray)</span></div></li><li data-sc="30107026" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Ukraine (Andrew) - Ghana (pimchik)</span></div></li><li data-sc="30107061" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Czechia (Smetana) - United States (Sheva)</span></div></li><li data-sc="30113805" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Newcastle UTD (FAITH) - Arsenal (POWER)</span></div></li><li data-sc="30113817" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Napoli (HORIZON) - Barcelona (EDEN)</span></div></li><li data-sc="30113991" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Atlanta United (NOBODY) - Los Angeles FC (APOLLO)</span></div></li><li data-sc="30113956" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Boca Juniors (Jindrich) - Palmeiras (Spike)</span></div></li><li data-sc="30114163" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>River Plate (Jadon) - Boca Juniors (Jindrich)</span></div></li><li data-sc="30114184" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Flamengo (Fede) - Palmeiras (Spike)</span></div></li><li data-sc="30114188" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Borussia Dortmund (Dante) - Eintracht Frankfurt (Ashton)</span></div></li><li data-sc="30114200" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Arsenal (Millie) - Manchester Utd (Florie)</span></div></li><li data-sc="30107210" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Memphis Grizzlies (Linkor) - Dallas Mavericks (MaaaS1K)</span></div></li><li data-sc="30107238" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Los Angeles Clippers (Mikki) - Milwaukee Bucks (Yaro)</span></div></li><li data-sc="30113617" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Memphis Grizzlies (Underrated) - Milwaukee Bucks (SPOOKY)</span></div></li><li data-sc="30113622" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Dallas Mavericks (GUARD) - Denver Nuggets (RAZE)</span></div></li><li data-sc="30113766" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Los Angeles Lakers (Karma) - Boston Celtics (Taapz)</span></div></li><li data-sc="30113789" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>Miami Heat (CRYPTO) - Toronto Raptors (CRUCIAL)</span></div></li><li data-sc="30114164" data-vt="2" class="jes str__list_item"><div><i class="ico-s mod-mod_118"></i><span>New York Knicks (Oscar) - Los Angeles Lakers (Damian)</span></div></li><li data-sc="c1745971210949721" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_27"></i><span>Carreras 24 h</span></div></li><li data-sc="c1745971212885707" data-vt="4" class="jes str__list_item"><div><i class="ico-s mod-mod_28"></i><span>Carreras 24 h</span></div></li></ul></div></div><div hidden="" class="jcr" data-cid="react_0HNCD4MK09B54" data-cn="$R.Jsx.s.streaming.StreamingEventList" data-cp="{&quot;initialData&quot;:{&quot;e&quot;:[{&quot;ty&quot;:2,&quot;c&quot;:&quot;30073173&quot;,&quot;t&quot;:&quot;D. Yastremska - A. Potapova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;WTA Roma&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30091676&quot;,&quot;t&quot;:&quot;Corinthians - Red Bull Bragantino&quot;,&quot;ic&quot;:&quot;1&quot;,&quot;st&quot;:&quot;Brasil Paulista Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30105993&quot;,&quot;t&quot;:&quot;Rogers, Anna / Sanchez, Ana Sofia - Motosono, Kianah / Schoppe, Ellie&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;ITF Indian Harbour Beach Femenino&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30095660&quot;,&quot;t&quot;:&quot;V. Dyrl - M. Unguryan&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30095386&quot;,&quot;t&quot;:&quot;S. Yakimenko - V. Kondratenko&quot;,&quot;ic&quot;:&quot;87&quot;,&quot;st&quot;:&quot;Setka Cup Masculina&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30106824&quot;,&quot;t&quot;:&quot;Spain (zoyir) - France (Serenity)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - International Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107326&quot;,&quot;t&quot;:&quot;Italy (Klever) - Germany (Samurai)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - International Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30106680&quot;,&quot;t&quot;:&quot;FC Porto (hotShot) - S.L. Benfica (LaikingDast)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Primeira Liga Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30106730&quot;,&quot;t&quot;:&quot;SC Braga (Kodak) - Sporting CP (Kray)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Primeira Liga Battle - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107026&quot;,&quot;t&quot;:&quot;Ukraine (Andrew) - Ghana (pimchik)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta International Battle 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107061&quot;,&quot;t&quot;:&quot;Czechia (Smetana) - United States (Sheva)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Volta International Battle 2x3 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113805&quot;,&quot;t&quot;:&quot;Newcastle UTD (FAITH) - Arsenal (POWER)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113817&quot;,&quot;t&quot;:&quot;Napoli (HORIZON) - Barcelona (EDEN)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113991&quot;,&quot;t&quot;:&quot;Atlanta United (NOBODY) - Los Angeles FC (APOLLO)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - GG League - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113956&quot;,&quot;t&quot;:&quot;Boca Juniors (Jindrich) - Palmeiras (Spike)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114163&quot;,&quot;t&quot;:&quot;River Plate (Jadon) - Boca Juniors (Jindrich)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114184&quot;,&quot;t&quot;:&quot;Flamengo (Fede) - Palmeiras (Spike)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114188&quot;,&quot;t&quot;:&quot;Borussia Dortmund (Dante) - Eintracht Frankfurt (Ashton)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valhalla Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114200&quot;,&quot;t&quot;:&quot;Arsenal (Millie) - Manchester Utd (Florie)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Efútbol - Valkiria Cup - 2x4 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107210&quot;,&quot;t&quot;:&quot;Memphis Grizzlies (Linkor) - Dallas Mavericks (MaaaS1K)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - NBA Battle - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30107238&quot;,&quot;t&quot;:&quot;Los Angeles Clippers (Mikki) - Milwaukee Bucks (Yaro)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - NBA Battle - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113617&quot;,&quot;t&quot;:&quot;Memphis Grizzlies (Underrated) - Milwaukee Bucks (SPOOKY)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113622&quot;,&quot;t&quot;:&quot;Dallas Mavericks (GUARD) - Denver Nuggets (RAZE)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113766&quot;,&quot;t&quot;:&quot;Los Angeles Lakers (Karma) - Boston Celtics (Taapz)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30113789&quot;,&quot;t&quot;:&quot;Miami Heat (CRYPTO) - Toronto Raptors (CRUCIAL)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - GG League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:2,&quot;c&quot;:&quot;30114164&quot;,&quot;t&quot;:&quot;New York Knicks (Oscar) - Los Angeles Lakers (Damian)&quot;,&quot;ic&quot;:&quot;118&quot;,&quot;st&quot;:&quot;Ebasket - Valhalla League - 4x5 mins.&quot;,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;es&quot;:null,&quot;t&quot;:null,&quot;l&quot;:[{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1745971210949721&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;27&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false},{&quot;ty&quot;:4,&quot;c&quot;:&quot;c1745971212885707&quot;,&quot;t&quot;:&quot;Streaming 24h&quot;,&quot;ic&quot;:&quot;28&quot;,&quot;st&quot;:null,&quot;cd&quot;:null,&quot;ip&quot;:false}],&quot;ine&quot;:false,&quot;hml&quot;:true},&quot;subscription&quot;:{&quot;type&quot;:14,&quot;param&quot;:{&quot;sdd&quot;:[],&quot;ste&quot;:[1],&quot;spe&quot;:null,&quot;cc&quot;:&quot;ES&quot;,&quot;ec&quot;:[&quot;3 W\u0026B&quot;,&quot;6 W\u0026B&quot;]}},&quot;wid&quot;:&quot;w_1-p_4-wt_6&quot;,&quot;selectedEvent&quot;:{&quot;sec&quot;:&quot;pse&quot;,&quot;ty&quot;:2,&quot;c&quot;:&quot;30073173&quot;,&quot;t&quot;:&quot;D. Yastremska - A. Potapova&quot;,&quot;ic&quot;:&quot;8&quot;,&quot;st&quot;:&quot;WTA Roma&quot;,&quot;cd&quot;:null,&quot;ip&quot;:true},&quot;hasVideoSelector&quot;:true,&quot;resources&quot;:{&quot;greyhounds&quot;:&quot;Galgos&quot;,&quot;horses&quot;:&quot;Caballos&quot;,&quot;greyhoundsAndHorses&quot;:&quot;Carreras 24 h&quot;,&quot;primeLabel&quot;:&quot;Prime&quot;},&quot;isPrimeEnabled&quot;:true}" data-co="false"></div>
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




    <div id="video" class="jintPlayer none" data-pt="1" data-pid="15" data-src="" data-prot="1" data-apiurl="https://wab.performfeeds.com/livestreamlaunch/1gjkdo1pbegih1g5qqlyjwqldf/9f6le1j3km0e15260qn93h74w?_fmt=json&amp;_fld=sl,aLng,pa,sTok,mFmt" data-apihead="{&quot;Authorization&quot;:&quot;Bearer S9lkZZjfdtGlKCiieLg8b75oSDVWBGZQ9hLaomJFT2QX3XtsK9ESG-aFAPaBODYAl_auR3_FJJxoUDZlMh1sV-FGWc3YLRVxpkfWq1_yHIRzzsmyRrhWpp3ZTcwFGF9zR4h9HJW1ld-jN_rUkqmUIl40M8KX-Z7jtqVFieoHWk6YA83I4wvIcUzZsPQxgFMIb9v6jysolU5yZjLPNj3lmErvvUAqjau9P20K_mg-mRtd57TyIstu3jQupCKlxHv7vTgFAXldChxbzDPb9DS1z5QSg0d_U5ZrKA8i3tz7jpLNBKw_cZIfrbsLRwv2ACnunpvxRwNaTBM8r49WC9h6Yw&quot;}" data-an="UA-34961270-1" data-drm="">

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

                <a href="/live/d-yastremska-a-potapova-sc30073173" class="str__bets-link jlink" title="D. Yastremska - A. Potapova">
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




    <div class="jdata" data-section="betslip" data-hash="z8ZXs2UbkTieIdWwvbUghWXHPhqVQSkkTU8T2S1_Moc"></div>

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
                    <span class="list-nav__numero">56</span>
                    <i class="ico-s icon-chevron-thin-right list-nav__arrow"></i>
                </a>
            </li>
            <li>
                <a href="/calendario" data-url="/calendario" class="jemptyp list-nav__item jt_bcIr" data-lnk="Calendario">
                    <i class="ico-m icon-calendar list-nav__icon"></i>
                    <span class="list-nav__texto text">
                        Hoy
                    </span>
                    <span class="list-nav__numero">346</span>
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
</div>    <div data-jsfile="betslip.section.js?v=z8ZXs2UbkTieIdWwvbUghWXHPhqVQSkkTU8T2S1_Moc" class="ljs" hidden="hidden"></div>
    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw4-3" data-v="{&quot;ParentHtmlId&quot;:&quot;w_3-p_4-wt_106_c&quot;,&quot;HtmlId&quot;:&quot;w_3-p_4-wt_106_c_Betslip&quot;,&quot;ClassName&quot;:&quot;betslip_container janimateSquare&quot;,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



    </section>

    <section id="w_14-p_4-wt_106_c" class="jqw  none  betslip_container betslip_container--userbets widget_type_106_c" data-wt="106" data-pa="4" data-co="0" data-po="14" data-sw="false" data-vi="False" data-sl="True" data-ti="False" data-sc="False" data-pwi="95" data-nrc="0" data-ic="true" data-vtw="null" data-sn="UserBets">




    <div class="jdata" data-section="userBets" data-hash="5RFWZowPD2P-Yt41H4kksEoERfQYRWC8L4gfmBKS6TM"></div>


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

<div data-jsfile="userBets.section.js?v=5RFWZowPD2P-Yt41H4kksEoERfQYRWC8L4gfmBKS6TM" class="ljs" hidden="hidden"></div>    <div data-jsfile="sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE" class="ljs" hidden="hidden"></div>


    <div hidden="" id="aw4-14" data-v="{&quot;DateFrom&quot;:&quot;2025-05-04T00:00:00&quot;,&quot;DateTo&quot;:&quot;2025-05-07T23:59:59&quot;,&quot;LastDays&quot;:0,&quot;StatusConfigurations&quot;:[{&quot;Status&quot;:3,&quot;ShowDateFilter&quot;:false,&quot;LastDays&quot;:null,&quot;IconClass&quot;:null},{&quot;Status&quot;:2,&quot;ShowDateFilter&quot;:false,&quot;LastDays&quot;:null,&quot;IconClass&quot;:null},{&quot;Status&quot;:4,&quot;ShowDateFilter&quot;:false,&quot;LastDays&quot;:30,&quot;IconClass&quot;:null},{&quot;Status&quot;:1,&quot;ShowDateFilter&quot;:true,&quot;LastDays&quot;:null,&quot;IconClass&quot;:&quot;ico-m icon-calendar&quot;}],&quot;Status&quot;:null,&quot;TabsClasses&quot;:null,&quot;ContainerClasses&quot;:&quot;ticket__userbets&quot;,&quot;TabsNavClasses&quot;:&quot;tab__group--fullwidth&quot;,&quot;AlwaysVisible&quot;:false,&quot;ShowNotLoggedInView&quot;:false,&quot;ParentHtmlId&quot;:null,&quot;HtmlId&quot;:null,&quot;ClassName&quot;:&quot;betslip_container betslip_container--userbets&quot;,&quot;VisibleTitleBox&quot;:false,&quot;TitleBox&quot;:null}"></div>



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
        <form class="modal__content animate" action="/deportes/baloncesto/nba/41" method="post">
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
<div data-jsfile="cookieConfigMessage.section.js?v=LVC4IzO-Axa8gi9eaU57o5RGb6rsfEXO4F-DbgtcJME" class="ljs" hidden="hidden"></div>

    <div>
    <div class="modal jmo modal_session" id="sessionCountdownMessage" style="display:none;">
    <div class="modal__wrapper">
        <form class="modal__content animate" action="/deportes/baloncesto/nba/41" method="post">
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
        <form class="modal__content animate" action="/deportes/baloncesto/nba/41" method="post">
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
          <a href="/esports" title="Apuestas de Esports">Apuestas de Esports</a>
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
</section>        <div hidden="" id="initHora" data-hour="23" data-min="52" data-sec="5"></div>
        <section class="footer__time">
            <div class="footer__time-box">
                <span id="hora">23:52:15</span>

    <div tabindex="0" class="select-noform select-noform-dark jdivtz ">
        <div class="select-noform_active">
            <span>(UTC+01:00) Bruselas, Copenhague, Madrid, París</span>
        </div>
        <ul id="tzlst" class="none select-noform__options ps_scroll ps"><div class="ps__rail-x" style="left: 0px; bottom: 0px;"><div class="ps__thumb-x" tabindex="0" style="left: 0px; width: 0px;"></div></div><div class="ps__rail-y" style="top: 0px; right: 0px;"><div class="ps__thumb-y" tabindex="0" style="top: 0px; height: 0px;"></div></div></ul>
    </div>

            </div>
            <div class="footer__lastlogin">



            </div>
        </section>
    <div class="modal jmo " style="display:none;">
    <div class="modal__wrapper">
        <form class="modal__content animate" action="/deportes/baloncesto/nba/41" method="post">
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

<div data-jsfile="chatBot2.section.js?v=s9oOooRpgzKYSKvD-51O4Yq7wPFBTEkKjN67mm4aIf0" class="ljs" hidden="hidden"></div>
    <img class="reta-square" src="/reta-square.jpg?638822515256060597" alt="Retabet square" style="max-width:0%">




    <div id="modalFactory">

        <div class="modal jmo jModal" style="display:none;">
            <div class="modal__wrapper">
                    <form class="modal__content animate jcontent jformModal" action="/deportes/baloncesto/nba/41" method="post">

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


<script src="https://rtds.retabet.es/Scripts/rtds.js?4"></script><script src="https://apuestas.retabet.es/js/modules/navMenu.section.js?v=tME5PzfZ54xGB269naOKpHK-RnwrxmnlnMGtNxgQjKk"></script><script src="https://apuestas.retabet.es/js/modules/login.section.js?v=rPzpL_sTWM0GPifOUxK26dWwAnxcJ4BAsLUCGgMlR1Q"></script><script src="https://apuestas.retabet.es/js/modules/forgotPassword.section.js?v=mKdHpqsS2l9rrlL-fyiMSkBfkPsjltOiQpbuvPWiuKY"></script><script src="https://apuestas.retabet.es/js/modules/esportsnav.section.js?v=CpxRLSHqJUNAOeZPMXmZJ7M1rTb8_2cw9Jso8XELkfM"></script><script src="https://apuestas.retabet.es/js/modules/header.section.js?v=Uucyabh6zg8iDg482ZXdQPbDlW0ReT91HH6XrlK8lVI"></script><script src="https://apuestas.retabet.es/js/modules/sportsbookMenu.widget.js?v=znjJeAaH-5uGyINB6dJiPjt-tbHyVTeZmmWC21-v1r8"></script><script src="https://apuestas.retabet.es/js/modules/sportsNoResult.section.js?v=PyjtOZ-2gadSXfwTIK7Ws1oMsxHKC1aEOAT2tBYnb48"></script><script src="https://apuestas.retabet.es/js/modules/sectionWrapper.widget.js?v=xxaM-WzvGe4qczxR6RkNOjhAIRt29kzxVJ5NaSvCXPE"></script><script src="https://apuestas.retabet.es/js/modules/sportsbookDate.section.js?v=QPr7o7VM8Y_cmKDfxSahqCh60fcI2qzXYlY3Rwc1ybg"></script><script src="https://apuestas.retabet.es/js/modules/sportsbookSubdiscipline.widget.js?v=0eN63JXlgxlluqC2ZwYdfY-n1VI8RoYwDRapos9eoEI"></script><script src="https://apuestas.retabet.es/js/modules/htmlContent.widget.js?v=8iumHKsvzpx5Nf4oqTAjAnlt1ASnbTT__lTcL-iNhaA"></script><script src="https://apuestas.retabet.es/js/modules/streaming.section.js?v=K9IXm3CDCeY7V2LPCt0n_uqSLa0Rayyp5b57q8Lt-Xk"></script><script src="https://apuestas.retabet.es/js/modules/streaming.widget.js?v=y6DsDbtcBFroCKpeEqKty8uFmvFPmuNsaRhIDA1X26c"></script><script src="https://apuestas.retabet.es/js/modules/quickGames.widget.js?v=HmlVpIfddkyYOkgAMPcyLlgAY_7yKDdSOXPCbhmoEUc"></script><script src="https://apuestas.retabet.es/js/modules/betslip.section.js?v=z8ZXs2UbkTieIdWwvbUghWXHPhqVQSkkTU8T2S1_Moc"></script><script src="https://apuestas.retabet.es/js/modules/userBets.section.js?v=5RFWZowPD2P-Yt41H4kksEoERfQYRWC8L4gfmBKS6TM"></script><script src="https://apuestas.retabet.es/js/modules/searcher.section.js?v=u_iuzCffABACpNOUqQuIv5nH1YJEH72wMOFJqu5etGU"></script><script src="https://apuestas.retabet.es/js/modules/cookieConfigMessage.section.js?v=LVC4IzO-Axa8gi9eaU57o5RGb6rsfEXO4F-DbgtcJME"></script><script src="https://apuestas.retabet.es/js/modules/casinoMessage.section.js?v=i5QENHiJ4mx5hJwYbRxUCOoX2q05PcIXDfGpWKa3jn0"></script><script src="https://apuestas.retabet.es/js/modules/footer.section.js?v=5czERWbmkzVlFPzd-dkWtxxyIaPG-f9BY6lDUNjSa4Q"></script><script src="https://apuestas.retabet.es/js/modules/chatBot2.section.js?v=s9oOooRpgzKYSKvD-51O4Yq7wPFBTEkKjN67mm4aIf0"></script><link rel="stylesheet" href="https://www.retabet.es/css/cookiemodal.css">
<div class="modal__cookies-allow jckModal" data-ckt="1" data-ckna="ac" data-ckvl="{ &quot;t&quot;: true, &quot;a&quot;: true, &quot;c&quot;: true }" data-ckexp="365" data-ckd=".retabet.es" data-ln="es-ES">
    <p>
        Utilizamos cookies propias y de terceros para analizar nuestros servicios y mostrarte anuncios basados en tus intereses. Puedes obtener más información, configurarlas o rechazar su uso pulsando <a class="jconf modal__cookies-allow__link-config" data-d="https://www.retabet.es/">AQUÍ</a>.
    </p>
    <div class="banner__cookies-botones">
            <button class="btn btn__secondary jreject">
                Rechazar
            </button>
       <button class="btn btn__secondary jaccept">
           Aceptar
       </button>
    </div>
</div><script src="https://static.xenioo.com/webchat/xenioowebchat.js" data-id="xenioo" data-node="app02"></script></body></html>

"""
from parsel import Selector
import re
import dateparser
import json
import ast
import datetime
import traceback
import pytz
from bookies_configurations import list_of_markets_V2

html_cleaner = re.compile("<.*?>")

response = Selector(response)
sport = "Football"
match_infos = []
list_of_markets = list_of_markets_V2["Luckia"]["1"]
# print("list_of_markets", list_of_markets)
match_infos = []

xpath_results = response.xpath("//li[@class='jlink jev event__item']").extract()
for xpath_result in xpath_results:
    try:
        xpath_result = Selector(xpath_result)
        home_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[0]
        away_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[1]
        url = xpath_result.xpath("//li[@class='jlink jev event__item']/@data-u").extract()[0]
        date = xpath_result.xpath("//span[@class='event__day']/text()").extract()[0]
        time = xpath_result.xpath("//span[@class='event__time']/text()").extract()[0]
        date = dateparser.parse(''.join(date + " " + time))
        if "/live/" not in url:
            match_infos.append(
                {"url": "https://apuestas.retabet.es" + url, "home_team": home_team, "away_team": away_team,
                 "date": date})
    except Exception as e:
        continue
        # print(e)

print(match_infos)
