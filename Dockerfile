# ==========================================================
# NOTE:
#     Using latest tag to get Python 3.9 security updates,
#     consciously disregarding SonarCloud issue docker:S6596
#     "Specific version tag for image should be used".
# ==========================================================
FROM registry.access.redhat.com/ubi9/python-39 AS appbase
# ==========================================================

# Setting file ownership to root:root and running the container
# as appuser:appuser, so that the files' permissions can't be
# changed afterwards as appuser (using file ownership).
#
# See SonarCloud issue docker:S6504 ("Allowing non-root users
# to modify resources copied to an image is security-sensitive"):
# https://rules.sonarsource.com/docker/RSPEC-6504/

ENV PYTHONUNBUFFERED 1

USER root
WORKDIR /app
RUN mkdir /entrypoint \
    # Mark the app directory as safe to get rid of git's
    # "fatal: detected dubious ownership in repository at '/app'" warning
    # when spinning up the container
    && git config --system --add safe.directory /app \
    # Create appuser group and user for running the app as non-root
    && groupadd --system appuser \
    && useradd --system --gid appuser --create-home appuser

COPY --chown=root:root requirements.txt /app/requirements.txt

RUN dnf update -y \
    && dnf install -y nc postgresql-devel \
    && pip install -U pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && dnf clean all

COPY --chown=root:root docker-entrypoint.sh /entrypoint/docker-entrypoint.sh
ENTRYPOINT ["/entrypoint/docker-entrypoint.sh"]

# ==============================
FROM appbase AS staticbuilder
# ==============================

ENV VAR_ROOT /app
COPY --chown=root:root . /app
RUN python manage.py collectstatic --noinput

# ==============================
FROM appbase AS development
# ==============================

COPY --chown=root:root requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r /app/requirements-dev.txt \
    && pip install --no-cache-dir pip-tools

ENV DEV_SERVER=1

# Copy all files not ignored by .dockerignore to container
# and make them readable & executable by everyone
COPY --chown=root:root . /app/
RUN chmod -R ugo=rX /app/

USER appuser:appuser

EXPOSE 8080/tcp

# ==============================
FROM appbase AS production
# ==============================

COPY --from=staticbuilder --chown=root:root /app/static /app/static

COPY --chown=root:root requirements-prod.txt /app/requirements-prod.txt
RUN pip install --no-cache-dir -r /app/requirements-prod.txt \
    && dnf clean all

# Copy all files not ignored by .dockerignore to container
# and make them readable & executable by everyone
COPY --chown=root:root . /app/
RUN chmod -R ugo=rX /app/

USER appuser:appuser

EXPOSE 8080/tcp
