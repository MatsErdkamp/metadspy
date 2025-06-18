---

## Extending Metadspy with Pipeline & Custom Modules


Here is what I have to do tomorrow:

1. Pipeline Modules

   * I will declare a new `Pipeline` type in the schema to chain sub‑modules.
   * I will enable specifying a list of step names and an iterate configuration (how many hops and which state variables to carry).
   * I will implement the `build` method to generate a DSPy class that loops through each step, feeding outputs back into shared state.

2. Custom Modules

   * I will introduce a `Custom` type that can import and instantiate a handwritten Python class or function.
   * I will allow passing any init arguments from YAML into the Python constructor.
   * This will serve as my escape hatch for logic that’s too complex to express declaratively.

3. Template Integration

   * I will update the Jinja templates to recognize both `Pipeline` and `Custom` types.
   * For `Pipeline`, I will render a class definition wiring sub‑modules and looping logic in `module.j2`.
   * For `Custom`, I will render direct import/instantiation of the user’s Python component.

4. Example Usage

   * I will define building‑block modules (query generator, search tool, note appender) under `modules:`.
   * In the top‑level `module:` section, I will declare either:

     * A **Pipeline** chaining those modules with iteration.
     * A **Custom** pointing to a standalone Python class when I need full control.

By doing this, I keep the core pipeline fully declarative in YAML while retaining the option to drop into Python code when necessary.
