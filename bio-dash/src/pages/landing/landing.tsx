import { Link } from "react-router-dom";
import { Card, CardContent } from "@mui/material";

export const Landing = () => {
  return (
    <div className="flex flex-col">
      <header className="px-4 lg:px-6 h-14 flex items-center">
        <Link className="flex items-center justify-center" to="#">
          <BeakerIcon className="h-6 w-6" />
          <span className="sr-only">Scientific SaaS</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            to="/upload"
          >
            Try Me
          </Link>
          <Link
            className="text-sm font-medium hover:underline underline-offset-4"
            to="#"
          >
            About Us
          </Link>
        </nav>
      </header>
      <main className="w-full mx-auto  ">
        <section className="w-full md:py-24 lg:py-32 border-y">
          <div className="container mx-auto">
            <div className="flex gap-4  sm:px-6 md:px-10 md:grid-cols-2 md:gap-16">
              <div>
                <h1 className="lg:leading-tighter text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl xl:text-[3.4rem] 2xl:text-[3.75rem] pb-2">
                  Unlock the Power of Scientific Computing
                </h1>
                <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400 pb-5">
                  Our scientific software as a service platform provides
                  powerful tools and algorithms to help you analyze data, run
                  simulations, and visualize results.
                </p>
                <div className="space-x-4">
                  <Link
                    className="inline-flex h-9 items-center justify-center rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-gray-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-50/90 dark:focus-visible:ring-gray-300"
                    to="#"
                  >
                    Get Started
                  </Link>
                  <Link
                    className="inline-flex h-9 items-center justify-center rounded-md border border-gray-200 bg-white px-4 py-2 text-sm font-medium shadow-sm transition-colors hover:bg-gray-100 hover:text-gray-900 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:border-gray-800 dark:bg-gray-950 dark:hover:bg-gray-800 dark:hover:text-gray-50 dark:focus-visible:ring-gray-300"
                    to="#"
                  >
                    Learn More
                  </Link>
                </div>
              </div>
              <img
                alt="Hero"
                className="mx-auto aspect-[3/1] overflow-hidden rounded-xl object-cover"
                height="300"
                src="./dams_hero.jpg"
                width="1270"
              />
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32" id="features">
          <div className="container space-y-12 px-4 md:px-6 mx-auto">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-gray-100 px-3 py-1 text-sm dark:bg-gray-800">
                  Key Features
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                  Powerful Tools for Scientific Computing
                </h2>
                <p className="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                  Our scientific software as a service platform provides a suite
                  of advanced tools and algorithms to help you tackle complex
                  scientific problems.
                </p>
              </div>
            </div>
            <div className="mx-auto grid items-start gap-8 sm:max-w-4xl sm:grid-cols-2 md:gap-12 lg:max-w-5xl lg:grid-cols-3">
              <div className="grid gap-1">
                <div className="flex items-center gap-2">
                  <AtomIcon className="h-6 w-6 text-gray-900 dark:text-gray-50" />
                  <h3 className="text-lg font-bold">Data Analysis</h3>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Leverage our advanced data analysis tools to uncover insights
                  and patterns in your scientific data.
                </p>
              </div>
              <div className="grid gap-1">
                <div className="flex items-center gap-2">
                  <PlayIcon className="h-6 w-6 text-gray-900 dark:text-gray-50" />
                  <h3 className="text-lg font-bold">Simulation</h3>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Run complex simulations and models to test hypotheses and
                  predict outcomes.
                </p>
              </div>
              <div className="grid gap-1">
                <div className="flex items-center gap-2">
                  <ViewIcon className="h-6 w-6 text-gray-900 dark:text-gray-50" />
                  <h3 className="text-lg font-bold">Visualization</h3>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Bring your data to life with our powerful visualization tools
                  and create stunning reports.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section
          className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800"
          id="testimonials"
        >
          <div className="container grid items-center justify-center gap-4 px-4 text-center md:px-6 mx-auto">
            <div className="space-y-3">
              <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">
                What Our Customers Say
              </h2>
              <p className="mx-auto max-w-[600px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                Hear from the scientists and researchers who have used our
                platform to power their work.
              </p>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              <Card className="h-full w-full">
                <CardContent className="space-y-4">
                  <blockquote className="text-lg font-semibold leading-snug">
                    “The data analysis tools in this platform have been
                    game-changing for our research team. We've been able to
                    uncover insights that would have taken us months to find
                    otherwise.”
                  </blockquote>
                  <div>
                    <div className="font-semibold">Dr. Emily Sharma</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Lead Researcher, Acme Labs
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="h-full w-full">
                <CardContent className="space-y-4">
                  <blockquote className="text-lg font-semibold leading-snug">
                    “The simulation capabilities of this platform have allowed
                    us to test our hypotheses much more efficiently. We've been
                    able to iterate on our models and get results faster than
                    ever before.”
                  </blockquote>
                  <div>
                    <div className="font-semibold">Dr. Liam Nguyen</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Computational Physicist, Quantum Labs
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="h-full w-full">
                <CardContent className="space-y-4">
                  <blockquote className="text-lg font-semibold leading-snug">
                    “The visualization tools in this platform have allowed us to
                    create stunning reports and presentations that really bring
                    our data to life. The ease of use and flexibility have been
                    incredibly valuable.”
                  </blockquote>
                  <div>
                    <div className="font-semibold">Dr. Olivia Gonzalez</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Senior Researcher, Bioinformatics Institute
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

function AtomIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="1" />
      <path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z" />
      <path d="M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z" />
    </svg>
  );
}

function BeakerIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4.5 3h15" />
      <path d="M6 3v16a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V3" />
      <path d="M6 14h12" />
    </svg>
  );
}

function PlayIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polygon points="5 3 19 12 5 21 5 3" />
    </svg>
  );
}

function ViewIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5 12s2.545-5 7-5c4.454 0 7 5 7 5s-2.546 5-7 5c-4.455 0-7-5-7-5z" />
      <path d="M12 13a1 1 0 1 0 0-2 1 1 0 0 0 0 2z" />
      <path d="M21 17v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2" />
      <path d="M21 7V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v2" />
    </svg>
  );
}
