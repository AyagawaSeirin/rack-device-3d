var boom_flag = 0;
$('#top_icon_2').on('click', function () {
  move_flag == 0 ? showOrHideMark(1, 'Markup Layer') : '';
  boom_flag = 1;
});
$('#top_icon_2_xs').on('click', function () {
  move_flag == 0 ? showOrHideMark(1, 'Markup Layer') : '';
  boom_flag = 1;
});
$('#top_icon_1').on('click', function () {
  showOrHideMark(1, 'Markup Layer');
  boom_flag = 0;
  nodeColor = [1, 1, 1, 0.5, 1, 1];
  $.each($('#menu-item-box1>.menu-item>input'), function (i, item) {
    $(item).parent().removeClass('active');
  });

  move_flag = 0;
  ivSetEditMode('select');
});
$('#top_icon_1_xs').on('click', function () {
  showOrHideMark(1, 'Markup Layer');
  boom_flag = 0;
  nodeColor = [1, 1, 1, 0.5, 1, 1];
  $.each($('#menu-item-box1>.menu-item>input'), function (i, item) {
    $(item).parent().removeClass('active');
  });

  move_flag = 0;
  ivSetEditMode('select');
});

$('.qrcode').qrcode({
  render: 'canvas',
  text: document.location.href,
  width: '150',
  height: '150',
  background: '#ffffff',
  foreground: '#000000',
});
$('#boomlicon5').hover(function () {
  $('.qr-container').toggle();
});

const el = document.getElementById('server-detail-header');
if (el) {
  el.innerHTML = ` <div class="header-right header-lang" id="header-lang-info">
    <img class="lang" src="../../../res/images/lang.svg" />
    <img class="lang mobile-lang" src="../../../res/images/mobile_lang.svg" />
    <span i18n="lang">简体中文</span>
    <img class="top" src="../../../res/images/top.svg" />
    <div class="chooseLang" id="langList">
      <div class="chooseLang-item" data-lang="cn">简体中文</div>
      <div class="chooseLang-item"  data-lang="en">English</div>
    </div>
  </div>
  <div class="header-right not-login" id="header-user-infor">
    <img class="user-icon" src="../../../res/images/user.svg" />
    <img id="mobile-user-icon" class="user-icon avatar-icon mobile-user-icon" src="../../../res/images/avatar.svg" />
    <span id="user_name" class="user-name">登录</span>
    <img class="top" src="../../../res/images/top.svg" />
    <div class="chooseLang login-drop-dow">
      <div class="chooseLang-item mobile-user-name" id="mobile-user-name"></div>
      <div class="chooseLang-item" id="login_out" i18n="loginOut">退出登录</div>
    </div>
  </div>`;
}
