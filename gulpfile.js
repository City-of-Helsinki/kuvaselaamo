'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

var pathScss = './src/hkm/hkm/static/hkm/scss/**/*.scss'
var pathCss = './src/hkm/hkm/static/hkm/css/'

gulp.task('sass', function () {
  return gulp.src(pathScss)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(pathCss));
});

gulp.task('sass:watch', function () {
  gulp.watch(pathScss, ['sass']);
});

gulp.task('default', ['sass', 'sass:watch']);
