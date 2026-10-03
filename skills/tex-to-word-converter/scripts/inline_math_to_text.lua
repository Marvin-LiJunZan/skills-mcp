-- Filter to convert inline LaTeX math to native formatted text runs (avoiding Office Math object)
-- Display math ($$...$$ or \begin{equation}) will be strictly kept as OMML/MathType equation objects.

local greek_map = {
  ["alpha"] = "α", ["beta"] = "β", ["gamma"] = "γ", ["delta"] = "δ", ["epsilon"] = "ε",
  ["varepsilon"] = "ε", ["zeta"] = "ζ", ["eta"] = "η", ["theta"] = "θ", ["vartheta"] = "θ",
  ["iota"] = "ι", ["kappa"] = "κ", ["lambda"] = "λ", ["mu"] = "μ", ["nu"] = "ν",
  ["xi"] = "ξ", ["pi"] = "π", ["varpi"] = "ϖ", ["rho"] = "ρ", ["varrho"] = "ϱ",
  ["sigma"] = "σ", ["varsigma"] = "ς", ["tau"] = "τ", ["upsilon"] = "υ", ["phi"] = "φ",
  ["varphi"] = "φ", ["chi"] = "χ", ["psi"] = "ψ", ["omega"] = "ω",
  ["Gamma"] = "Γ", ["Delta"] = "Δ", ["Theta"] = "Θ", ["Lambda"] = "Λ", ["Xi"] = "Ξ",
  ["Pi"] = "Π", ["Sigma"] = "Σ", ["Upsilon"] = "Υ", ["Phi"] = "Φ", ["Psi"] = "Ψ", ["Omega"] = "Ω"
}

local sym_map = {
  ["pm"] = "±", ["times"] = "×", ["div"] = "÷", ["cdot"] = "·", ["leq"] = "≤",
  ["le"] = "≤", ["geq"] = "≥", ["ge"] = "≥", ["neq"] = "≠", ["ne"] = "≠",
  ["approx"] = "≈", ["sim"] = "~", ["infty"] = "∞", ["nabla"] = "∇", ["partial"] = "∂",
  ["in"] = "∈", ["leftarrow"] = "←", ["rightarrow"] = "→", ["leftrightarrow"] = "↔"
}

function Math(elem)
  if elem.mathtype == "InlineMath" then
    local t = elem.text:match("^%s*(.-)%s*$")
    
    -- Case 1: Pure single Greek letter or Math Symbol
    local clean_name = t:gsub("^\\", "")
    if greek_map[clean_name] then
      return pandoc.Emph({pandoc.Str(greek_map[clean_name])})
    elseif sym_map[clean_name] then
      return pandoc.Str(sym_map[clean_name])
    end
    
    -- Case 2: Variable with subscript: e.g. \sigma_3, \sigma_{3}, \varepsilon_a, c_u, E_s, F_s, p'
    local var, sub = t:match("^\\?([%a%']+)[_%^]([%a%d%']+)$")
    local is_sub = t:find("_")
    local is_sup = t:find("%^")
    
    if not var then
      var, sub = t:match("^\\?([%a%']+)[_%^]%{(.-)%}$")
    end
    
    if var and sub then
      local clean_var = var:gsub("^\\", "")
      local clean_sub = sub:gsub("^\\", "")
      local base_str = greek_map[clean_var] or var
      local sub_str = greek_map[clean_sub] or sub
      
      if is_sub then
        return {
          pandoc.Emph({pandoc.Str(base_str)}),
          pandoc.Subscript({pandoc.Str(sub_str)})
        }
      elseif is_sup then
        if sub_str == "circ" or sub_str == "\\circ" then
          return { pandoc.Emph({pandoc.Str(base_str)}), pandoc.Str("°") }
        else
          return {
            pandoc.Emph({pandoc.Str(base_str)}),
            pandoc.Superscript({pandoc.Str(sub_str)})
          }
        end
      end
    end

    -- Case 3: Single Roman variable: $c$, $d$, $t$, $x$, $y$, $z$, $p'$, $q$, $u$
    if t:match("^[%a]%'?$") then
      return pandoc.Emph({pandoc.Str(t)})
    end
    
    -- Case 4: Number with symbol: e.g. \pm 0.3, 10\%
    if t:match("^\\pm%s*([%d%.]+)$") then
      local num = t:match("^\\pm%s*([%d%.]+)$")
      return pandoc.Str("± " .. num)
    end
  end
  return elem
end
