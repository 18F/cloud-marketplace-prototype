'use strict';

const path = require('path');
const gulp = require('gulp');
const gutil = require('gulp-util');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');

const USWDS_DIST = 'node_modules/uswds/dist';
const USWDS_DIST_DIR = path.join(__dirname, ...USWDS_DIST.split('/'));
const STATIC_DIR = './marketplace/static/marketplace';

gulp.task('copy-uswds-assets', () => {
  return gulp.src(`${USWDS_DIST}/@(js|fonts|img)/**/**`)
  .pipe(gulp.dest(`${STATIC_DIR}/vendor/uswds`));
});

gulp.task('sass', () => {
  return gulp.src('./sass/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        path.join(USWDS_DIST_DIR, 'scss'),
      ]
    }).on('error', sass.logError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(`${STATIC_DIR}/css`));
});

gulp.task('watch', ['sass', 'copy-uswds-assets'], () => {
  gulp.watch('./sass/**/*.scss', ['sass']);
});

gulp.task('build', ['sass', 'copy-uswds-assets']);

gulp.task('default', ['build']);
