require 'parslet'

module Ash
  class Parser < Parslet::Parser
    rule(:ws) { match('\s').repeat(1) }
    rule(:ws?) { ws.maybe }

    rule(:ka) { str('ka') >> ws? }
    rule(:ko) { str('ko') >> ws? }
    rule(:kun) { str('kun') >> ws? }

    rule(:word) { match('[a-z\-]').repeat(1) >> ws? }
    rule(:verb) { str('na').maybe >> str('v') >> word }
    rule(:noun) { str('s') >> word }
    rule(:adjective) { str('l') >> word }

    rule(:noun1) { noun.as(:noun) >> adjective.repeat.as(:adjectives) }
    rule(:possessor) { ko >> noun1.as(:possessor) }
    rule(:noun_phrase) { noun1.as(:head) >> possessor.repeat.as(:possessors).maybe }

    rule(:temporal_adjunct) { (str('timet') | str('timem') | str('time')) >> ws? >> noun_phrase }
    rule(:instrumental_adjunct) { str('tem') >> str('na').maybe >> ws? >> noun_phrase }
    rule(:causal_adjunct) { (str('tozem') | str('tozet')) >> ws? >> clause }
    rule(:adjunct) { temporal_adjunct | instrumental_adjunct | causal_adjunct }

    rule(:verb_phrase) {
      verb.as(:verb) >>
      (noun_phrase.as(:object) >> (kun >> noun_phrase.as(:indirect_object)).maybe).maybe >>
      adjunct.repeat.as(:adjuncts)
    }

    rule(:clause) { noun_phrase.as(:subject) >> verb_phrase.as(:verb_phrase) }

    rule(:statement) { clause.as(:statement) }
    rule(:command) { verb_phrase.as(:command) }
    rule(:question) { ka >> clause.as(:question) }
    rule(:sentence) { statement | command | question }

    root(:sentence)

    def parse(str)
      transform_ast(super(str))
    end

    private

      def transform_ast(ast)
        case ast
        when Parslet::Slice then ast.to_s.strip
        when String then ast.strip
        when Hash then Hash[ast.map { |key, child| [key, transform_ast(child)] }]
        when Array then ast.map { |child| transform_ast(child) }
        else raise StandardError, "Don't know how to walk this: #{ast.class.inspect}"
        end
      end

  end
end
