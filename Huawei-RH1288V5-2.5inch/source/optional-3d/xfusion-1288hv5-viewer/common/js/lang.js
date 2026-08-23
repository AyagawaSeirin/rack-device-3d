const title = {
  cn: '3D模型',
  en: '3D Model',
};
var stories = {
  cn: 'https://e.huawei.com/cn/case-studies?product=servers',
  en: 'https://e.huawei.com/en/case-studies?product=servers',
};
$(document).ready(function () {
  /*默认语言*/
  // $("#langList").css({display:'none'})
  var state = {
    title: document.title,
    url: document.location.href,
    otherkey: null,
  };
  var langIndex = window.location.href.indexOf('?lang');
  function initHref() {
    if (langIndex != -1) {
      defaultLang = window.location.href.substr(langIndex + 6, 2);
      $('.moreHref').attr('href', moreHref[defaultLang]);
    } else {
      history.replaceState(state, document.title, document.location.href + '?lang=' + defaultLang); //初始化地址栏
    }
  }
  function preventBlank(choose) {
    if ($(choose).attr('href') == '#') {
      $(choose).attr('target', '_self');
    }
  }
  function check() {
    $('[i18n]').i18n({
      defaultLang: defaultLang,
      filePath: './res/i18n/',
      filePrefix: 'i18n_',
      fileSuffix: '',
      forever: false,
      callback: function () {},
    });
    var URL = './res/i18n/i18n_' + defaultLang + '.json?v=' + new Date().getTime(); //完成tip的国际化
    $.ajax({
      type: 'GET',
      url: URL,
      success: function (e) {
        langJson = e;
        setSeverTitle(location.href, defaultLang);
        $.each($('.i18n'), function (i, item) {
          var key = $(item).attr('i18nkey');
          $(item).attr('data-original-title', e[key]);
        });
       setTimeout(()=>{
        $('.menu-item>span').each((index,item)=>{
          $(item).prev().prev().attr('title',  $(item).html());
        })
       },500)
        history.replaceState(state, document.title, state.url.substring(langIndex, 0) + '?lang=' + defaultLang); //改变化地址栏
        $('title').html(title[defaultLang]);
        $('.moreHref').attr('href', moreHref[defaultLang]);
        preventBlank('.moreHref');

        $('.tools').attr('href', tools[defaultLang]);
        preventBlank('.tools');

        $('.userguide').attr('href', userguide[defaultLang]);
        preventBlank('.userguide');

        $('.software').attr('href', software[defaultLang]);
        preventBlank('.software');

        $('#top_icon_4').attr('href', Specifications[defaultLang]);
        preventBlank('#top_icon_4');

        $('.stories').attr('href', stories[defaultLang]);
        preventBlank('.stories');
        $('.qrcode').qrcode({
          render: 'canvas',
          text: document.location.href,
          width: '150',
          height: '150',
          background: '#ffffff',
          foreground: '#000000',
        });
        $('.qrcode canvas').css({ display: 'none' });
        $('.qrcode canvas:last-child').css({ display: 'inline-block' }); //隐藏前面的二维码，只显示当前的（也就是最后一个）
        const isLogin =JSON.parse( sessionStorage.getItem('isLogin'));
        const nameEl = document.getElementById('user_name');
        if (!isLogin) {
          nameEl.innerText =langJson.login;
        }
      },
    });
     document.documentElement.dataset.lang = defaultLang
    if (moreHref[defaultLang] == '#' || moreHref[defaultLang] == '') {
      $('.moreHref').parent('.menu-item').hide();
    } else {
      $('.moreHref').parent('.menu-item').show();
    }

    if (tools[defaultLang] == '#' || tools[defaultLang] == '') {
      $('.tools').parent('.menu-item').hide();
    } else {
      $('.tools').parent('.menu-item').show();
    }
    if (userguide[defaultLang] == '#' || userguide[defaultLang] == '') {
      $('.userguide').parent('.menu-item').css('display', 'none');
    } else {
      $('.userguide').parent('.menu-item').show();
    }
    if (software[defaultLang] == '#' || software[defaultLang] == '') {
      $('.software').parent('.menu-item').hide();
    } else {
      $('.software').parent('.menu-item').show();
    }
    if (stories[defaultLang] == '#' || stories[defaultLang] == '') {
      $('.stories').parent('.menu-item').hide();
    } else {
      $('.stories').parent('.menu-item').show();
    }
    if (Specifications[defaultLang] == '#' || Specifications[defaultLang] == '') {
      $('#top_icon_4').parent().hide();
    } else {
      $('#top_icon_4').parent().show();
    }


  }
  initHref();
  check();
  $('#langList').on('click', function (e) {
    defaultLang = $(e.target).attr('data-lang');
    check();
    if (defaultLang === 'cn') {
      $('.title-cn')?.css({ display: 'inline-block' });
      $('.title-en')?.css({ display: 'none' });
      document.documentElement.dataset.lang = 'cn'

    } else {
      $('.title-cn')?.css({ display: 'none' });
      $('.title-en')?.css({ display: 'inline-block' });
      document.documentElement.dataset.lang = 'en'
    }
   
  });
  $('#top_icon_8').on('click', function (e) {
    var hasDetaiList = ['taishan2280', 'taishan5280', 'atlas8009000', 'atlas8009000', 'atlas900pod', 'atlas900pod'];
    e.preventDefault();
    var url = '';
    var backDetail = false;
    for (var i = 0; i < hasDetaiList.length; i++) {
      if (window.location.href.indexOf(hasDetaiList[i]) > -1) {
        sessionStorage.setItem('whitchDetail', hasDetaiList[i]);
        backDetail = hasDetaiList[i];
        break;
      }
    }
    if (backDetail) {
      //如果该机型有详情页
      if (defaultLang == 'cn') {
        url = '../../../detail/detail' + '_zh.html?model=' + backDetail;
      }
      if (defaultLang == 'en') {
        url = '../../../detail/detail' + '_en.html?model=' + backDetail;
      }
    } else {
      if (defaultLang == 'cn') {
        url = '../../../index' + '_zh.html';
      }
      if (defaultLang == 'en') {
        url = '../../../index' + '_en.html';
      }
    }
    window.location = url;
  });
  function setSeverTitle(url, defaultLang) {
    const regex = /\/([\w-]+)\/index.html/; // 正则表达式匹配 "/xxxxx/index.html" 中的 "xxxxx"
    const match = regex.exec(url);
    $.ajax({
      type: 'GET',
      url: '../../../res/js/index-data.json',
      success: function (list) {
        const fileName = match[1];
        if (fileName) {
          const server = list.find((item) => item.file === fileName);
          if (defaultLang === 'cn') {
            $('.navbar-brand p').html(server.displayNameZh || server.displayNameEn);
            return;
          }
          $('.navbar-brand p').html(server.displayNameEn);
        }
      },
    });

    //
  }
});
