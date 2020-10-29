Preparing docker images for integration tests
=============================================

Our test suite relies heavily on custom docker images for testing. The main
reason that we use custom images is test speed: having prepared docker images
vs. building them on each test execution saves a ton of time.

Adding a new image is relatively straightforward process. We can just copy one
of the preexisting definitions from the *docker* directory and update it. All
docker files should have a name in the format of ``<name>-<tag>.docker``.

To build and publish our image, we can run the *docker/build.sh* script::

   $ cd docker
   $ ./build.sh sensu-5.21.0

Note that the command will add a *sensu-go-tests-* prefix to all images. In
the previous example, the build script will build the
*quay.io/xlab-steampunk/sensu-go-tests-sensu:5.21.0* image.
