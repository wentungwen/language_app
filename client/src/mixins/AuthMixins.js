export default {
  data() {
    return {
      is_logged_in: this.get_cookie("token") ? true : false,
    };
  },
  methods: {
    set_cookie(name, value, days = 7) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      const expires = `expires=${date.toUTCString()}`;
      document.cookie = `${name}=${value};${expires};path=/`;
    },
    get_cookie(name) {
      const cookieName = `${name}=`;
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.indexOf(cookieName) === 0) {
          return cookie.substring(cookieName.length, cookie.length);
        }
      }
      return null;
    },
    delete_cookie(name) {
      const expires = "expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie = `${name}=; ${expires}`;
    },
  },
};
