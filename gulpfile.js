var gulp = require("gulp"),
    plug = require("gulp-load-plugins")();

var src = {
  coffee: "src/kawaz/statics/coffee/**/**.coffee",
  less: "src/kawaz/statics/less/**/**.less",
  template: "src/kawaz/templates/**/**.html",
  bootstrapjs: [
          "vendor/bootstrap/js/transition.js",
          "vendor/bootstrap/js/alert.js",
          "vendor/bootstrap/js/button.js",
          "vendor/bootstrap/js/carousel.js",
          "vendor/bootstrap/js/collapse.js",
          "vendor/bootstrap/js/dropdown.js",
          "vendor/bootstrap/js/modal.js",
          "vendor/bootstrap/js/tooltip.js",
          "vendor/bootstrap/js/popover.js",
          "vendor/bootstrap/js/scrollspy.js",
          "vendor/bootstrap/js/tab.js",
          "vendor/bootstrap/js/affix.js"
    ],
  bootstrapfont: "vendor/bootstrap/fonts/*"
};

var dest = {
  js: "src/kawaz/statics/js",
  css: "src/kawaz/statics/css",
  font: "src/kawaz/statics/fonts"
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

gulp.task("bootstrap-js-concat", function () {
  var stream = gulp.src(src.bootstrapjs)
      .pipe(plug.plumber())
      .pipe(plug.concat("bootstrap.js"))
      .pipe(gulp.dest(dest.js));

  if (~ this.seq.indexOf("watch"))
    stream.pipe(plug.livereload());
});

gulp.task("bootstrap-copy-font", function() {
  gulp.src(src.bootstrapfont)
    .pipe(plug.plumber())
    .pipe(gulp.dest(dest.font));
});

gulp.task("default", ["coffee", "less", "bootstrap-js-concat", "bootstrap-copy-font"]);

gulp.task("watch", ["default"], function () {
  gulp.watch(src.coffee, ["coffee"]);
  gulp.watch(src.less, ["less"]);
  gulp.watch(src.template, ["template"]);
  gulp.watch(src.bootstrapjs, ["bootstrap-js-concat"]);
  gulp.watch(src.bootstrapfont, ["bootstrap-copy-font"]);
});
