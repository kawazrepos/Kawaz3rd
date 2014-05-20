var gulp = require("gulp"),
    concat = require("gulp-concat"),
    plug = require("gulp-load-plugins")();

var src = {
  coffee: "src/kawaz/statics/coffee/**/**.coffee",
  less: "src/kawaz/statics/less/**/**.less",
  template: "src/kawaz/templates/**/**.html",
  bootstrapjs: "vendor/bootstrap/js/*.js"
};

var dest = {
  js: "src/kawaz/statics/js",
  css: "src/kawaz/statics/css"
};

gulp.task("coffee", function () {
  plug.watch({glob: src.coffee})
      .pipe(plug.plumber())
      .pipe(plug.coffee({bare: true}))
      .pipe(gulp.dest(dest.js))
      .pipe(plug.livereload());
});

gulp.task("less", function () {
  plug.watch({glob: src.less})
      .pipe(plug.plumber())
      .pipe(plug.less())
      .pipe(gulp.dest(dest.css))
      .pipe(plug.livereload());
});

gulp.task("template", function () {
  plug.watch({glob: src.template})
      .pipe(plug.plumber())
      .pipe(plug.livereload());
});

gulp.task("bootstrapjsconcat", function () {
  gulp.src(src.bootstrapjs)
      .pipe(plug.plumber())
      .pipe(concat("bootstrap.js"))
      .pipe(gulp.dest(dest.js));
});

gulp.task("default", ["coffee", "less", "template", "bootstrapjsconcat"]);
