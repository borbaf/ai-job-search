import { describe, expect, test } from "bun:test"
import { spawnSync } from "child_process"
import { resolve } from "path"

const CLI_PATH = resolve(__dirname, "../src/cli.ts")

describe("getonbrd-cli", () => {
  test("shows help when invoked with --help", () => {
    const res = spawnSync("bun", ["run", CLI_PATH, "--help"], { encoding: "utf-8" })
    expect(res.status).toBe(0)
    expect(res.stdout).toContain("Get on Board")
    expect(res.stdout).toContain("search")
    expect(res.stdout).toContain("detail")
  })

  test("runs search with json output", () => {
    const res = spawnSync("bun", ["run", CLI_PATH, "search", "-q", "Data", "--limit", "2"], {
      encoding: "utf-8",
    })
    expect(res.status).toBe(0)
    const json = JSON.parse(res.stdout)
    expect(Array.isArray(json)).toBe(true)
    expect(json.length).toBeGreaterThan(0)
    expect(json[0]).toHaveProperty("id")
    expect(json[0]).toHaveProperty("title")
    expect(json[0]).toHaveProperty("company")
    expect(json[0]).toHaveProperty("url")
  })
})
