'use strict';

const gulp = require('gulp');
const sass = require('gulp-sass');

const pathScss = './hkm/static/hkm/scss/**/*.scss';
const pathCss = './hkm/static/hkm/css/';
const pathStaticrootCss = './staticroot/hkm/css/';

gulp.task('sass', function() {
  return gulp.src(pathScss)
      .pipe(sass())
      .pipe(gulp.dest(pathCss))
      .pipe(gulp.dest(pathStaticrootCss))
})

gulp.task('sass:watch', function() {
  gulp.watch(pathScss, gulp.series(['sass']));
})

gulp.task('default', gulp.series(['sass', 'sass:watch']))