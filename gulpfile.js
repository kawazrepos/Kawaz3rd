var gulp = require("gulp"),
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
  var stream = gulp.src(src.coffee)
      .pipe(plug.plumber())
      .pipe(plug.coffee({bare: true}))
      .pipe(gulp.dest(dest.js));

  if (~ this.seq.indexOf("watch"))
    stream.pipe(plug.livereload());
});

gulp.task("less", function () {
  var stream = gulp.src(src.less)
      .pipe(plug.plumber())
      .pipe(plug.less())
      .pipe(gulp.dest(dest.css));

  if (~ this.seq.indexOf("watch"))
    stream.pipe(plug.livereload());
});

gulp.task("template", function () {
  gulp.src(src.template)
      .pipe(plug.plumber())
      .pipe(plug.livereload());
});

gulp.task("bootstrapjsconcat", function () {
  var stream = gulp.src(src.bootstrapjs)
      .pipe(plug.plumber())
      .pipe(plug.concat("bootstrap.js"))
      .pipe(gulp.dest(dest.js));

  if (~ this.seq.indexOf("watch"))
    stream.pipe(plug.livereload());
});

gulp.task("default", ["coffee", "less", "bootstrapjsconcat"]);

gulp.task("watch", ["default"], function () {
  gulp.watch(src.coffee, ["coffee"]);
  gulp.watch(src.less, ["less"]);
  gulp.watch(src.template, ["template"]);
  gulp.watch(src.bootstrapjs, ["bootstrapjsconcat"]);
});
