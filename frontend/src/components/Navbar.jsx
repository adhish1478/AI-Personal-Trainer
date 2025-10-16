export default function Navbar() {
  return (
    <nav className="w-full bg-white shadow-sm fixed top-0 left-0 z-50 p-4 flex justify-center">
      <div className="w-full max-w-5xl flex justify-between items-center">
        <section className="flex items-center">
            <img src="./src/assets/logo.png" alt="Logo" className="w-8 h-8 inline-block mr-2"/>
            <h1 className="text-xl font-bold text-green-600">Evolve</h1>
        </section>
        <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700 transition">
          Login
        </button>
      </div>
    </nav>
  );
}