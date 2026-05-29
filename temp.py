# non-unique: 'Invalid: Username already exists'
# has spaces: 'Invalid: Username cannot have spaces'
# outside of length: 'Invalid: Username must be 1-15 characters long'
# valid: 'Valid'

# Do not edit the next line:
def register(username, users):
    
  # Write your code here:
  if username in users:
      print('Invalid: Username already exists')
  # Check if username has spaces
  elif ' ' in username:
      print('Invalid: Username cannot have spaces')
  elif not username or len(username) < 1 or len(username) > 15:
      print('Invalid: Username must be 1-15 characters long')
  else: print('Valid')
register("JoltCrate", ['NovaRift', 'PixelFox', 'AeroMint', 'ByteLynx', 'CrimsonIQ', 'EchoVale', 'FrostByte', 'GlintRush', 'HexaBloom', 'IronPulse', 'JadeCircuit', 'KiloNova', 'LunarZip', 'MysticOrb', 'NeonDrift', 'OrbitCraze', 'PlasmaJet', 'QuantumYak', 'RapidVibe', 'SolarNix', 'TurboLeaf', 'UltraPebble', 'VaporNest', 'WildComet', 'XenonTrail', 'YellowFlux', 'ZenithBug', 'AlphaTwig', 'BlazeRoot', 'CyberMoth'])
register("LunarZip", ['NovaRift', 'PixelFox', 'AeroMint', 'ByteLynx', 'CrimsonIQ', 'EchoVale', 'FrostByte', 'GlintRush', 'HexaBloom', 'IronPulse', 'JadeCircuit', 'KiloNova', 'LunarZip', 'MysticOrb', 'NeonDrift', 'OrbitCraze', 'PlasmaJet', 'QuantumYak', 'RapidVibe', 'SolarNix', 'TurboLeaf', 'UltraPebble', 'VaporNest', 'WildComet', 'XenonTrail', 'YellowFlux', 'ZenithBug', 'AlphaTwig', 'BlazeRoot', 'CyberMoth'])
register("BrickNova", ['NovaRift', 'PixelFox', 'AeroMint', 'ByteLynx', 'CrimsonIQ', 'EchoVale', 'FrostByte', 'GlintRush', 'HexaBloom', 'IronPulse', 'JadeCircuit', 'KiloNova', 'LunarZip', 'MysticOrb', 'NeonDrift', 'OrbitCraze', 'PlasmaJet', 'QuantumYak', 'RapidVibe', 'SolarNix', 'TurboLeaf', 'UltraPebble', 'VaporNest', 'WildComet', 'XenonTrail', 'YellowFlux', 'ZenithBug', 'AlphaTwig', 'BlazeRoot', 'CyberMoth'])