var gulp = require("gulp"),
    plug = require("gulp-load-plugins")();

// use livereload?
var livereload = false;

var bootstrapjsprefix = "vendor/bootstrap/js/";

var src = {
  coffee: "src/kawaz/statics/coffee/**/**.coffee",
  less: "src/kawaz/statics/less/**/**.less",
  template: "src/kawaz/templates/**/**.html",
  bootstrapjs: [
          //transition.jsを先頭にしてjsの結合を行わないと
          //BootstrapベースのCSS3アニメーションが動かない
          //トラブルが発生したのと、本家のjs結合gruntfile
          //も、このような結合の仕方になっていたのでそれに
          //ならう実装にする
          //tooltip.jsをpopover.jsよりも先に結合しないと
          //正しく動作しないトラブルが発生するのでそれを
          //防ぐために先にtooltip.jsを読み込ませる
          bootstrapjsprefix + "transition.js",
          bootstrapjsprefix + "tooltip.js",
          bootstrapjsprefix + "*.js"
  ],
  bootstrapfont: "vendor/bootstrap/fonts/*",
  mace: "node_modules/mace/build/mace.min.js"
};

var dest = {
  js: "src/kawaz/statics/js",
  css: "src/kawaz/statics/css",
  font: "src/kawaz/statics/fonts",
  vendor: "src/kawaz/statics/vendor"
};

gulp.task("coffee", function () {
  var stream = gulp.src(src.coffee)
      .pipe(plug.plumber())
      .pipe(plug.coffee({bare: true}))
      .pipe(gulp.dest(dest.js));

  if (livereload)
    stream.pipe(plug.livereload());
});

gulp.task("less", function () {
  var stream = gulp.src(src.less)
      .pipe(plug.plumber())
      .pipe(plug.less())
      .pipe(gulp.dest(dest.css));

  if (livereload)
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

  if (livereload)
    stream.pipe(plug.livereload());
});

gulp.task("bootstrap-copy-font", function() {
  gulp.src(src.bootstrapfont)
    .pipe(plug.plumber())
    .pipe(gulp.dest(dest.font));
});

gulp.task("mace-copy", function () {
  gulp.src(src.mace)
      .pipe(plug.plumber())
      .pipe(gulp.dest(dest.vendor));
});

gulp.task("default", ["coffee", "less", "bootstrap-js-concat", "bootstrap-copy-font", "mace-copy"]);

gulp.task("watch", ["default"], function () {
  livereload = true;
  plug.livereload();

  gulp.watch(src.coffee, ["coffee"]);
  gulp.watch(src.less, ["less"]);
  gulp.watch(src.template, ["template"]);
  gulp.watch(src.bootstrapjs, ["bootstrap-js-concat"]);
  gulp.watch(src.bootstrapfont, ["bootstrap-copy-font"]);
});
