/**
 * --------------- ChatTutor.org ----------------
 * Configuration file for chattutor.min.js which 
 * should not be modified. This file consists of
 * the necesary configurations for running chat-
 * tutor in a course.
 * Currently the ChatTutor needs be added by hand
 * or using the install.py script in each page of
 * the application, weather build with jupyter or
 * other frameworks.
 * The style necesary for ChatTutor is provided in
 * chattutor.style.css, and can be adjusted for 
 * every course's needs.
 * 
 * The following configuration variables have the
 * following meaning:
 * 
 * EMBEDDING_COLLECTION_NAME: the name of the
 * database that is [[either provided on
 * ChatTutor.org when an account is created and
 * a new course added - this will be added soon]]
 * or provided by the contributors to ChatTutor.
 * 
 * TEST_MODE: should be false for prodction and
 * either true or false for testing. When true,
 * requests to the chattutor server are actually
 * done to https://localhost:<SERVER_PORT>. 
 * This option is added because currently ChatTutor
 * has a CORS wall that only allows certain domains
 * to make requests to its APIs, and the CORS needs
 * to be manually updated when a course is ready
 * to use Chattutor. For testing purposes on should
 * run the ChatTutor server on the port SERVER_PORT
 * and request to it. This will be deprecated in
 * the latter phases of the project, when the CORS
 * will be updated automatically, and it is currently
 * used by our team for manually adding and testing 
 * ChatTutor to new courses.
 * 
 * COURSE_URL: the base url for the course
 * 
 * SERVER_PORT: the port listen to Chattutor 
 * server if ran locally. Used ONLY for testing
 * purposes
 */
const EMBEDDING_COLLECTION_NAME = "photonicsbootcamp12";
const TEST_MODE = true;
const COURSE_URL = "https://byucamacholab.github.io/Photonics-Bootcamp"
const SERVER_PORT = 5000
/**
 * --------------- TESTING CONFIGS ----------------
 * ChatTutor can be embedded on default applications
 * that run on servers, or in static pages such as
 * Jupyter Notebooks.
 * 
 * For the purpose of testing, the build method needs 
 * to be specified so the server knows how to parse
 * the current url name.
 * 
 * BUILT_WITH: "JUPYTER-NOTEBOOK"|"SERVER"
 * 
 * This configuration is ONLY used for testing and
 * will have no weight in production mode 
 * (TEST_MODE = false)
 */
const BUILT_WITH = "JUPYTER-NOTEBOOK"
/**
 * JUPYTER-NOTEBOOK Specific configurations.
 */
const BUILD_HTML_JUPYTER_NOTEBOOK_FOLDER = "_build/html"
