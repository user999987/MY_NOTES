Gradle is a combination of all Gradle properties set on the command line and your gradle.properties files. If an option is configured in multiple locations, the first one found in any of these locations wins:

* command line, as set using the -P / --project-prop environment options.
* gradle.properties in GRADLE_USER_HOME directory.
* gradle.properties in project root directory.
* gradle.properties in Gradle installation directory.