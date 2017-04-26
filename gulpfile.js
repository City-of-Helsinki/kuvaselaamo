'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

var pathScss = './hkm/static/hkm/scss/**/*.scss';
var pathCss = './hkm/static/hkm/css/';
var pathStaticrootCss = './staticroot/hkm/css/';

gulp.task('sass', function () {
  return gulp.src(pathScss)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(pathCss))
    .pipe(gulp.dest(pathStaticrootCss));
});

gulp.task('sass:watch', function () {
  gulp.watch(pathScss, ['sass']);
});

gulp.task('default', ['sass', 'sass:watch']);
