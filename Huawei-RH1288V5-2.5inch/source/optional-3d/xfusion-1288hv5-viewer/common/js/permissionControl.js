const originName = window.location.origin;
const pathname = window.location.pathname;
// const isMobile = window.innerWidth <= 768;
// const servers = ['1258hv7', '2258v7', '2258hv7', '1158hv7'];
const servers = [];
let startIndex = pathname.indexOf('server/');
let lastIndex = -1;
let currentServer = '';
if (startIndex !== -1) {
  startIndex += 7;
  lastIndex = pathname.indexOf('/index');
  currentServer = pathname.slice(startIndex, lastIndex);
}

const summerLogin = function () {
  const url = location.href;
  if (originName.indexOf('beta') > -1 || originName.indexOf('localhost') > -1) {
    window.location.href = 'http://uniportal.beta.xfusion.com/uniportal1?redirect=' + encodeURIComponent(url);
  } else {
    window.location.href = 'https://uniportal.xfusion.com/uniportal1?redirect=' + encodeURIComponent(url);
  }
};
const summerLogout = function () {
  const url = location.href;
  if (originName.indexOf('beta') > -1 || originName.indexOf('localhost') > -1) {
    window.location.href = 'http://uniportal.beta.xfusion.com/uniportal1/logout?redirect=' + encodeURIComponent(url);
  } else {
    window.location.href = 'https://uniportal.xfusion.com/uniportal1/logout?redirect=' + encodeURIComponent(url);
  }
};
function getUserInfor() {
  const noControl = startIndex === -1 || !servers.includes(currentServer);
  getToken().then(
    (token) => {
      if (noControl) {
        return;
      }
      if (token) {
        getUserLevel(token).then((level) => {
          if (level !== '1') {
            backHome();
          }
        }, backHome);
        return;
      }
      backHome();
    },
    () => {
      if (noControl) {
        return;
      }
      backHome();
    }
  );
}
function getToken() {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: originName + '/support/doc/rest/v1/user/loginStatus',
      type: 'GET',
      async: false,
      xhrFields: {
        withCredentials: true,
      },
      success: function (res, status, xhr) {
        const token = xhr.getResponseHeader('Token');
        getUserName(token);
        resolve(token);
      },
      error: () => {
        setUserName();
        reject();
      },
    });
  });
}
function getUserLevel(token) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: originName + '/support/doc/rest/v1/user/level',
      type: 'GET',
      async: false,
      xhrFields: {
        withCredentials: true,
      },
      headers: {
        Authorization: token,
      },
      success: function (res) {
        resolve(res.data);
      },
      error: () => {
        reject();
      },
    });
  });
}

function getUserName(token) {
  if (!token) {
    setUserName();
    return;
  }
  $.ajax({
    url: originName + '/support/doc/rest/v1/user/info',
    type: 'GET',
    async: false,
    xhrFields: {
      withCredentials: true,
    },
    headers: {
      Authorization: token,
    },
    success: function (res) {
      setUserName(res.data.givenName || res.data.displayName);
    },
    error: () => {
      setUserName();
    },
  });
}

function backHome() {
  if (startIndex === -1) {
    return;
  }
  let qs = location.search;
  let lang = new URLSearchParams(qs).get('lang');
  if (lang === 'en') {
    window.location.href = location.origin + '/server-3D/index_en.html';
    return;
  }
  window.location.href = location.origin + '/server-3D/index_zh.html';
}

function setUserName(name) {
  document.addEventListener('DOMContentLoaded', function() {
    const userInfoEl = document.getElementById('header-user-infor');
    
    if (!userInfoEl) {
      return;
    }
    const nameEl = document.getElementById('user_name');
    const mobileNameEl = document.getElementById('mobile-user-name');
    const mobileUserIcon = document.getElementById('mobile-user-icon');
    if (name) {
      userInfoEl.classList.remove('not-login');
      nameEl.innerText = name;
      mobileNameEl.innerText = name;
      const loginOutEl = document.getElementById('login_out');
      loginOutEl.onclick = () => {
        summerLogout();
      };
      nameEl.onclick = null;
      mobileUserIcon.onclick = null;
      sessionStorage.setItem('isLogin', true);
      return;
    }
    sessionStorage.setItem('isLogin', false);
    nameEl.onclick = () => {
      summerLogin();
    };
    mobileUserIcon.onclick = () => {
      summerLogin();
    };
  });
}

getUserInfor();
