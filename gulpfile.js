var gulp = require("gulp"),
    plug = require("gulp-load-plugins")();

var src = {
  coffee: "src/statics/coffee/**/**.coffee",
  less: "src/statics/less/**/**.less"
};

var dest = {
  js: "src/statics/js",
  css: "src/statics/css"
};

gulp.task("coffee", function () {
  plug.watch({glob: src.coffee})
      .pipe(plug.plumber())
      .pipe(plug.coffee({bare: true}))
      .pipe(gulp.dest(dest.js));
});

gulp.task("less", function () {
  plug.watch({glob: src.less})
      .pipe(plug.plumber())
      .pipe(plug.less())
      .pipe(gulp.dest(dest.css));
});

gulp.task("default", ["coffee", "less"]);
